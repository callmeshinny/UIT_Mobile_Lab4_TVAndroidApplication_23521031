package com.callmeshinny.tvandroidapplication

import android.app.Activity
import android.content.Intent
import android.graphics.BitmapFactory
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import java.net.URL

class MainActivity : Activity() {

    private lateinit var heroBackdrop: ImageView
    private lateinit var heroTitle: TextView
    private lateinit var heroMeta: TextView
    private lateinit var heroOverview: TextView
    private lateinit var statusText: TextView
    private lateinit var movieGridContainer: LinearLayout

    private var selectedCard: LinearLayout? = null
    private var selectedMovieId: Int = -1
    private var lastClickMovieId: Int = -1
    private var lastClickTime: Long = 0L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        heroBackdrop = findViewById(R.id.heroBackdrop)
        heroTitle = findViewById(R.id.heroTitle)
        heroMeta = findViewById(R.id.heroMeta)
        heroOverview = findViewById(R.id.heroOverview)
        statusText = findViewById(R.id.statusText)
        movieGridContainer = findViewById(R.id.movieGridContainer)

        loadMoviesFromTmdb()
    }

    private fun loadMoviesFromTmdb() {
        statusText.text = "Loading movies from TMDB..."

        Thread {
            try {
                val movies = TmdbApiClient.getPopularMovies()

                runOnUiThread {
                    statusText.text = "Popular Movies"
                    renderMovieGrid(movies)

                    if (movies.isNotEmpty()) {
                        showMovie(movies.first())
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    statusText.text = "Cannot load TMDB data"
                    heroTitle.text = "TMDB Error"
                    heroMeta.text = "Please check internet or token"
                    heroOverview.text = e.message ?: "Unknown error"
                }
            }
        }.start()
    }

    private fun renderMovieGrid(movieList: List<Movie>) {
        movieGridContainer.removeAllViews()

        movieList.chunked(3).forEach { rowMovies ->
            val row = LinearLayout(this).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply {
                    setMargins(0, 0, 0, 22)
                }
            }

            rowMovies.forEach { movie ->
                val card = LinearLayout(this).apply {
                    orientation = LinearLayout.VERTICAL
                    isClickable = true
                    isFocusable = true
                    isFocusableInTouchMode = true
                    background = getDrawable(R.drawable.movie_card_background)
                    setPadding(10, 10, 10, 14)

                    layoutParams = LinearLayout.LayoutParams(
                        0,
                        LinearLayout.LayoutParams.WRAP_CONTENT,
                        1f
                    ).apply {
                        setMargins(10, 0, 10, 0)
                    }
                }

                val image = ImageView(this).apply {
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        145
                    )
                    scaleType = ImageView.ScaleType.CENTER_CROP
                    background = getDrawable(R.drawable.poster_placeholder)
                    isClickable = true
                }

                val title = TextView(this).apply {
                    text = movie.title
                    textSize = 14f
                    maxLines = 2
                    setTextColor(getColor(R.color.white))
                    typeface = Typeface.DEFAULT_BOLD
                    setPadding(6, 10, 6, 0)
                    isClickable = true
                }

                val meta = TextView(this).apply {
                    val year = movie.releaseDate.take(4).ifBlank { "N/A" }
                    text = "$year  •  Rating ${String.format("%.1f", movie.voteAverage)}"
                    textSize = 12f
                    setTextColor(getColor(R.color.mutedText))
                    setPadding(6, 4, 6, 0)
                    isClickable = true
                }

                val clickListener = View.OnClickListener {
                    handleMovieClick(movie, card)
                }

                card.setOnClickListener(clickListener)
                image.setOnClickListener(clickListener)
                title.setOnClickListener(clickListener)
                meta.setOnClickListener(clickListener)

                card.setOnFocusChangeListener { view, hasFocus ->
                    view.background = when {
                        movie.id == selectedMovieId -> getDrawable(R.drawable.movie_card_selected_background)
                        hasFocus -> getDrawable(R.drawable.movie_card_focused_background)
                        else -> getDrawable(R.drawable.movie_card_background)
                    }

                    if (hasFocus) {
                        showMovie(movie)
                    }
                }

                card.addView(image)
                card.addView(title)
                card.addView(meta)
                row.addView(card)

                loadImageInto(movie.backdropPath ?: movie.posterPath, image)
            }

            if (rowMovies.size < 3) {
                repeat(3 - rowMovies.size) {
                    row.addView(View(this).apply {
                        layoutParams = LinearLayout.LayoutParams(0, 1, 1f).apply {
                            setMargins(10, 0, 10, 0)
                        }
                    })
                }
            }

            movieGridContainer.addView(row)
        }
    }

    private fun handleMovieClick(movie: Movie, card: LinearLayout) {
        val now = System.currentTimeMillis()
        val doubleClick = movie.id == lastClickMovieId && now - lastClickTime <= 900

        selectedMovieId = movie.id
        selectedCard?.background = getDrawable(R.drawable.movie_card_background)
        selectedCard = card
        card.background = getDrawable(R.drawable.movie_card_selected_background)

        showMovie(movie)

        if (doubleClick) {
            openMovieDetail(movie)
        }

        lastClickMovieId = movie.id
        lastClickTime = now
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

    private fun showMovie(movie: Movie) {
        heroTitle.text = movie.title

        val year = movie.releaseDate.take(4).ifBlank { "Unknown" }
        heroMeta.text = "$year   •   TMDB Rating ${String.format("%.1f", movie.voteAverage)}"
        heroOverview.text = movie.overview.ifBlank { "No overview available." }

        loadImageInto(movie.backdropPath ?: movie.posterPath, heroBackdrop)
    }

    private fun loadImageInto(path: String?, imageView: ImageView) {
        if (path.isNullOrBlank()) return

        Thread {
            try {
                val imageUrl = TmdbApiClient.IMAGE_BASE_URL + path
                val bitmap = BitmapFactory.decodeStream(URL(imageUrl).openStream())

                runOnUiThread {
                    imageView.setImageBitmap(bitmap)
                }
            } catch (_: Exception) {
            }
        }.start()
    }
}

