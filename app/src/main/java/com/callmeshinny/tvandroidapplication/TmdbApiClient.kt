package com.callmeshinny.tvandroidapplication

import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object TmdbApiClient {
    private const val BASE_URL = "https://api.themoviedb.org/3"
    const val IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w780"

    fun getPopularMovies(): List<Movie> {
        val token = BuildConfig.TMDB_ACCESS_TOKEN

        if (token.isBlank()) {
            throw IllegalStateException("Missing TMDB_ACCESS_TOKEN in local.properties")
        }

        val url = URL("$BASE_URL/movie/popular?language=en-US&page=1")
        val connection = url.openConnection() as HttpURLConnection

        connection.requestMethod = "GET"
        connection.setRequestProperty("accept", "application/json")
        connection.setRequestProperty("Authorization", "Bearer $token")
        connection.connectTimeout = 15000
        connection.readTimeout = 15000

        val responseCode = connection.responseCode
        val stream = if (responseCode in 200..299) {
            connection.inputStream
        } else {
            connection.errorStream
        }

        val body = stream.bufferedReader().use { it.readText() }

        if (responseCode !in 200..299) {
            throw IllegalStateException("TMDB API error $responseCode: $body")
        }

        val json = JSONObject(body)
        val results = json.getJSONArray("results")
        val movies = mutableListOf<Movie>()

        for (i in 0 until results.length()) {
            val item = results.getJSONObject(i)

            movies.add(
                Movie(
                    id = item.optInt("id"),
                    title = item.optString("title"),
                    overview = item.optString("overview"),
                    releaseDate = item.optString("release_date"),
                    voteAverage = item.optDouble("vote_average"),
                    posterPath = item.optString("poster_path").takeIf { it != "null" && it.isNotBlank() },
                    backdropPath = item.optString("backdrop_path").takeIf { it != "null" && it.isNotBlank() }
                )
            )
        }

        return movies
    }
}
