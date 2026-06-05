from pathlib import Path

pkg = Path("app/src/main/java/com/callmeshinny/tvandroidapplication")
res = Path("app/src/main/res")
layout = res / "layout"
drawable = res / "drawable"

layout.mkdir(parents=True, exist_ok=True)
drawable.mkdir(parents=True, exist_ok=True)

# selected pink border
(drawable / "movie_card_selected_background.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#171B25" />
    <stroke android:width="5dp" android:color="#FF244C" />
    <corners android:radius="10dp" />
</shape>
""", encoding="utf-8")

# detail screen layout
(layout / "activity_movie_detail.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#090B12">

    <ImageView
        android:id="@+id/detailBackdrop"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:alpha="0.42"
        android:scaleType="centerCrop" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:padding="34dp">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="MyMovie"
            android:textColor="#FF244C"
            android:textSize="30sp"
            android:textStyle="bold" />

        <Space
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_weight="1" />

        <TextView
            android:id="@+id/detailTitle"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Movie Title"
            android:textColor="#FFFFFF"
            android:textSize="42sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/detailMeta"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:text="TMDB"
            android:textColor="#FFFFFF"
            android:textSize="17sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/detailOverview"
            android:layout_width="860dp"
            android:layout_height="wrap_content"
            android:layout_marginTop="16dp"
            android:lineSpacingExtra="5dp"
            android:maxLines="5"
            android:text="Overview"
            android:textColor="#FFFFFF"
            android:textSize="17sp" />

        <TextView
            android:id="@+id/trailerStatus"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="18dp"
            android:text="Loading trailer..."
            android:textColor="#FFB3C5"
            android:textSize="14sp" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="14dp"
            android:orientation="horizontal">

            <Button
                android:id="@+id/watchButton"
                android:layout_width="190dp"
                android:layout_height="54dp"
                android:backgroundTint="#FF244C"
                android:text="Watch Trailer"
                android:textAllCaps="false"
                android:textColor="#FFFFFF"
                android:textStyle="bold" />

            <Button
                android:id="@+id/backButton"
                android:layout_width="140dp"
                android:layout_height="54dp"
                android:layout_marginStart="14dp"
                android:backgroundTint="#222A3A"
                android:text="Back"
                android:textAllCaps="false"
                android:textColor="#FFFFFF"
                android:textStyle="bold" />
        </LinearLayout>
    </LinearLayout>
</FrameLayout>
""", encoding="utf-8")

# detail activity
(pkg / "MovieDetailActivity.kt").write_text("""package com.callmeshinny.tvandroidapplication

import android.app.Activity
import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import java.net.URL

class MovieDetailActivity : Activity() {

    private var movieId: Int = -1
    private var trailerKey: String? = null

    private lateinit var detailBackdrop: ImageView
    private lateinit var detailTitle: TextView
    private lateinit var detailMeta: TextView
    private lateinit var detailOverview: TextView
    private lateinit var watchButton: Button
    private lateinit var backButton: Button
    private lateinit var trailerStatus: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_movie_detail)

        movieId = intent.getIntExtra("id", -1)
        val title = intent.getStringExtra("title") ?: "Movie"
        val overview = intent.getStringExtra("overview") ?: "No overview available."
        val releaseDate = intent.getStringExtra("releaseDate") ?: ""
        val voteAverage = intent.getDoubleExtra("voteAverage", 0.0)
        val backdropPath = intent.getStringExtra("backdropPath")
        val posterPath = intent.getStringExtra("posterPath")

        detailBackdrop = findViewById(R.id.detailBackdrop)
        detailTitle = findViewById(R.id.detailTitle)
        detailMeta = findViewById(R.id.detailMeta)
        detailOverview = findViewById(R.id.detailOverview)
        watchButton = findViewById(R.id.watchButton)
        backButton = findViewById(R.id.backButton)
        trailerStatus = findViewById(R.id.trailerStatus)

        detailTitle.text = title
        detailMeta.text = "${releaseDate.take(4).ifBlank { "Unknown" }}   •   TMDB Rating ${String.format("%.1f", voteAverage)}"
        detailOverview.text = overview

        loadImageInto(backdropPath ?: posterPath, detailBackdrop)
        loadTrailerKey()

        watchButton.setOnClickListener {
            val key = trailerKey
            if (key.isNullOrBlank()) {
                Toast.makeText(this, "Trailer is still loading or unavailable", Toast.LENGTH_SHORT).show()
            } else {
                startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://www.youtube.com/watch?v=$key")))
            }
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun loadTrailerKey() {
        trailerStatus.text = "Loading trailer..."

        Thread {
            try {
                val key = TmdbApiClient.getMovieTrailerKey(movieId)
                runOnUiThread {
                    trailerKey = key
                    trailerStatus.text = if (key.isNullOrBlank()) "No official trailer found" else "Trailer ready"
                }
            } catch (_: Exception) {
                runOnUiThread {
                    trailerStatus.text = "Cannot load trailer"
                }
            }
        }.start()
    }

    private fun loadImageInto(path: String?, imageView: ImageView) {
        if (path.isNullOrBlank()) return

        Thread {
            try {
                val bitmap = BitmapFactory.decodeStream(URL(TmdbApiClient.IMAGE_BASE_URL + path).openStream())
                runOnUiThread {
                    imageView.setImageBitmap(bitmap)
                }
            } catch (_: Exception) {
            }
        }.start()
    }
}
""", encoding="utf-8")

# patch MainActivity
main = pkg / "MainActivity.kt"
text = main.read_text(encoding="utf-8")

text = text.replace(
    "import android.app.Activity",
    "import android.app.Activity\nimport android.content.Intent"
)

text = text.replace(
    "private lateinit var movieGridContainer: LinearLayout",
    """private lateinit var movieGridContainer: LinearLayout

    private var selectedMovieId: Int = -1
    private var lastClickMovieId: Int = -1
    private var lastClickTime: Long = 0L
    private var selectedCard: LinearLayout? = null"""
)

old_click = """setOnClickListener {
                        showMovie(movie)
                        Toast.makeText(this@MainActivity, movie.title, Toast.LENGTH_SHORT).show()
                    }"""

new_click = """setOnClickListener {
                        handleMovieClick(movie, this)
                    }"""

text = text.replace(old_click, new_click)

image_old_click = """setOnClickListener {
                        showMovie(movie)
                        Toast.makeText(this@MainActivity, movie.title, Toast.LENGTH_SHORT).show()
                    }"""

image_new_click = """setOnClickListener {
                        handleMovieClick(movie, card)
                    }"""

text = text.replace(image_old_click, image_new_click)

insert_methods = """
    private fun handleMovieClick(movie: Movie, card: LinearLayout) {
        val now = System.currentTimeMillis()
        val isDoubleClick = movie.id == lastClickMovieId && now - lastClickTime < 650

        selectCard(movie, card)
        showMovie(movie)

        if (isDoubleClick) {
            openMovieDetail(movie)
        } else {
            Toast.makeText(this, "Tap again to open ${movie.title}", Toast.LENGTH_SHORT).show()
        }

        lastClickMovieId = movie.id
        lastClickTime = now
    }

    private fun selectCard(movie: Movie, card: LinearLayout) {
        selectedMovieId = movie.id
        selectedCard?.background = getDrawable(R.drawable.movie_card_background)
        selectedCard = card
        card.background = getDrawable(R.drawable.movie_card_selected_background)
    }

    private fun openMovieDetail(movie: Movie) {
        val intent = Intent(this, MovieDetailActivity::class.java).apply {
            putExtra("id", movie.id)
            putExtra("title", movie.title)
            putExtra("overview", movie.overview)
            putExtra("releaseDate", movie.releaseDate)
            putExtra("voteAverage", movie.voteAverage)
            putExtra("posterPath", movie.posterPath)
            putExtra("backdropPath", movie.backdropPath)
        }
        startActivity(intent)
    }

"""

if "private fun handleMovieClick" not in text:
    text = text.replace("    private fun showMovie(movie: Movie) {", insert_methods + "    private fun showMovie(movie: Movie) {")

main.write_text(text, encoding="utf-8")

# patch TmdbApiClient
tmdb = pkg / "TmdbApiClient.kt"
t = tmdb.read_text(encoding="utf-8")

if "fun getMovieTrailerKey" not in t:
    t = t.rsplit("}", 1)[0] + """
    fun getMovieTrailerKey(movieId: Int): String? {
        val token = BuildConfig.TMDB_ACCESS_TOKEN

        if (token.isBlank()) {
            throw IllegalStateException("Missing TMDB_ACCESS_TOKEN in local.properties")
        }

        val url = URL("$BASE_URL/movie/$movieId/videos?language=en-US")
        val connection = url.openConnection() as HttpURLConnection

        connection.requestMethod = "GET"
        connection.setRequestProperty("accept", "application/json")
        connection.setRequestProperty("Authorization", "Bearer $token")
        connection.connectTimeout = 15000
        connection.readTimeout = 15000

        val responseCode = connection.responseCode
        val stream = if (responseCode in 200..299) connection.inputStream else connection.errorStream
        val body = stream.bufferedReader().use { it.readText() }

        if (responseCode !in 200..299) {
            throw IllegalStateException("TMDB API error $responseCode: $body")
        }

        val results = JSONObject(body).getJSONArray("results")

        for (i in 0 until results.length()) {
            val item = results.getJSONObject(i)
            val site = item.optString("site")
            val type = item.optString("type")
            val official = item.optBoolean("official")
            val key = item.optString("key")

            if (site == "YouTube" && type == "Trailer" && official && key.isNotBlank()) {
                return key
            }
        }

        for (i in 0 until results.length()) {
            val item = results.getJSONObject(i)
            val site = item.optString("site")
            val key = item.optString("key")

            if (site == "YouTube" && key.isNotBlank()) {
                return key
            }
        }

        return null
    }
}
"""
    tmdb.write_text(t, encoding="utf-8")

# manifest
manifest = Path("app/src/main/AndroidManifest.xml")
m = manifest.read_text(encoding="utf-8")

if "MovieDetailActivity" not in m:
    m = m.replace(
        "<activity\n            android:name=\"com.callmeshinny.tvandroidapplication.MainActivity\"",
        "<activity\n            android:name=\"com.callmeshinny.tvandroidapplication.MovieDetailActivity\"\n            android:exported=\"false\"\n            android:screenOrientation=\"landscape\" />\n\n        <activity\n            android:name=\"com.callmeshinny.tvandroidapplication.MainActivity\""
    )

manifest.write_text(m, encoding="utf-8")

print("Done: pink selected border, double click detail screen, trailer button.")

