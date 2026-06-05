from pathlib import Path

pkg = Path("app/src/main/java/com/callmeshinny/tvandroidapplication")
res = Path("app/src/main/res")
layout = res / "layout"
drawable = res / "drawable"

layout.mkdir(parents=True, exist_ok=True)
drawable.mkdir(parents=True, exist_ok=True)

(drawable / "movie_card_selected_background.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#171B25" />
    <stroke android:width="5dp" android:color="#FF244C" />
    <corners android:radius="10dp" />
</shape>
""", encoding="utf-8")

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

        <Button
            android:id="@+id/watchButton"
            android:layout_width="190dp"
            android:layout_height="54dp"
            android:layout_marginTop="20dp"
            android:backgroundTint="#FF244C"
            android:text="Watch Trailer"
            android:textAllCaps="false"
            android:textColor="#FFFFFF"
            android:textStyle="bold" />

        <Button
            android:id="@+id/backButton"
            android:layout_width="140dp"
            android:layout_height="54dp"
            android:layout_marginTop="10dp"
            android:backgroundTint="#222A3A"
            android:text="Back"
            android:textAllCaps="false"
            android:textColor="#FFFFFF"
            android:textStyle="bold" />

    </LinearLayout>
</FrameLayout>
""", encoding="utf-8")

(pkg / "MovieDetailActivity.kt").write_text("""package com.callmeshinny.tvandroidapplication

import android.app.Activity
import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import java.net.URL

class MovieDetailActivity : Activity() {

    private lateinit var detailBackdrop: ImageView
    private lateinit var detailTitle: TextView
    private lateinit var detailMeta: TextView
    private lateinit var detailOverview: TextView
    private lateinit var watchButton: Button
    private lateinit var backButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_movie_detail)

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

        detailTitle.text = title
        detailMeta.text = "${releaseDate.take(4).ifBlank { "Unknown" }}   •   TMDB Rating ${String.format("%.1f", voteAverage)}"
        detailOverview.text = overview

        loadImageInto(backdropPath ?: posterPath, detailBackdrop)

        watchButton.setOnClickListener {
            val query = Uri.encode("$title official trailer")
            val url = "https://www.youtube.com/results?search_query=$query"
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
        }

        backButton.setOnClickListener {
            finish()
        }
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

manifest = Path("app/src/main/AndroidManifest.xml")
m = manifest.read_text(encoding="utf-8")

if "MovieDetailActivity" not in m:
    m = m.replace(
        '<activity\n            android:name="com.callmeshinny.tvandroidapplication.MainActivity"',
        '<activity\n            android:name="com.callmeshinny.tvandroidapplication.MovieDetailActivity"\n            android:exported="false"\n            android:screenOrientation="landscape" />\n\n        <activity\n            android:name="com.callmeshinny.tvandroidapplication.MainActivity"'
    )

manifest.write_text(m, encoding="utf-8")

main = pkg / "MainActivity.kt"
text = main.read_text(encoding="utf-8")

if "import android.content.Intent" not in text:
    text = text.replace("import android.app.Activity", "import android.app.Activity\nimport android.content.Intent")

main.write_text(text, encoding="utf-8")

print("Fixed missing selected border and MovieDetailActivity.")

