package com.callmeshinny.tvandroidapplication

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
