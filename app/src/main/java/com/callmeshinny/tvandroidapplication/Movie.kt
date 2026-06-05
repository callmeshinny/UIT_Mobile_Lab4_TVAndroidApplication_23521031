package com.callmeshinny.tvandroidapplication

data class Movie(
    val id: Int,
    val title: String,
    val overview: String,
    val releaseDate: String,
    val voteAverage: Double,
    val posterPath: String?,
    val backdropPath: String?
)
