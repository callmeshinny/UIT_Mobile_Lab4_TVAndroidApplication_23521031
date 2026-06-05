from pathlib import Path
import re

APP_DIR = Path("app")
PKG_DIR = APP_DIR / "src/main/java/com/callmeshinny/tvandroidapplication"
RES_DIR = APP_DIR / "src/main/res"

PKG_DIR.mkdir(parents=True, exist_ok=True)
(RES_DIR / "layout").mkdir(parents=True, exist_ok=True)
(RES_DIR / "values").mkdir(parents=True, exist_ok=True)
(RES_DIR / "drawable").mkdir(parents=True, exist_ok=True)
(RES_DIR / "mipmap-hdpi").mkdir(parents=True, exist_ok=True)
Path("screenshots").mkdir(exist_ok=True)

# ----------------------------
# Movie.kt
# ----------------------------
(PKG_DIR / "Movie.kt").write_text("""package com.callmeshinny.tvandroidapplication

data class Movie(
    val title: String,
    val year: String,
    val genre: String,
    val rating: String,
    val duration: String,
    val description: String,
    val posterSymbol: String
)
""", encoding="utf-8")

# ----------------------------
# MovieRepository.kt
# ----------------------------
(PKG_DIR / "MovieRepository.kt").write_text("""package com.callmeshinny.tvandroidapplication

object MovieRepository {
    val movies = listOf(
        Movie(
            title = "Interstellar",
            year = "2014",
            genre = "Sci-Fi / Adventure / Drama",
            rating = "8.7",
            duration = "2h 49m",
            description = "A group of explorers travel through a wormhole in space to find a new home for humanity.",
            posterSymbol = "🚀"
        ),
        Movie(
            title = "Spider-Man: Into the Spider-Verse",
            year = "2018",
            genre = "Animation / Action / Adventure",
            rating = "8.4",
            duration = "1h 57m",
            description = "Miles Morales becomes Spider-Man and joins other Spider-heroes from different dimensions.",
            posterSymbol = "🕷️"
        ),
        Movie(
            title = "Inside Out",
            year = "2015",
            genre = "Animation / Comedy / Family",
            rating = "8.1",
            duration = "1h 35m",
            description = "The emotions inside a young girl's mind help her deal with a major life change.",
            posterSymbol = "💭"
        ),
        Movie(
            title = "The Lion King",
            year = "1994",
            genre = "Animation / Adventure / Drama",
            rating = "8.5",
            duration = "1h 28m",
            description = "A young lion prince learns about responsibility, courage, and his place in the circle of life.",
            posterSymbol = "🦁"
        ),
        Movie(
            title = "Coco",
            year = "2017",
            genre = "Animation / Adventure / Music",
            rating = "8.4",
            duration = "1h 45m",
            description = "A young boy enters the Land of the Dead and discovers the importance of family and memory.",
            posterSymbol = "🎸"
        ),
        Movie(
            title = "Avatar",
            year = "2009",
            genre = "Sci-Fi / Action / Fantasy",
            rating = "7.9",
            duration = "2h 42m",
            description = "A marine on an alien planet becomes involved with the Na'vi and the fight to protect Pandora.",
            posterSymbol = "🌌"
        ),
        Movie(
            title = "Harry Potter and the Sorcerer's Stone",
            year = "2001",
            genre = "Fantasy / Adventure / Family",
            rating = "7.6",
            duration = "2h 32m",
            description = "A young boy discovers that he is a wizard and begins his journey at Hogwarts School.",
            posterSymbol = "⚡"
        ),
        Movie(
            title = "Toy Story",
            year = "1995",
            genre = "Animation / Adventure / Comedy",
            rating = "8.3",
            duration = "1h 21m",
            description = "A cowboy doll feels threatened when a new space toy becomes his owner's favorite.",
            posterSymbol = "🤠"
        )
    )
}
""", encoding="utf-8")

# ----------------------------
# MainActivity.kt
# ----------------------------
(PKG_DIR / "MainActivity.kt").write_text("""package com.callmeshinny.tvandroidapplication

import android.app.Activity
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.KeyEvent
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView

class MainActivity : Activity() {

    private lateinit var movieListContainer: LinearLayout
    private lateinit var selectedTitle: TextView
    private lateinit var selectedMeta: TextView
    private lateinit var selectedDescription: TextView
    private lateinit var selectedPoster: TextView
    private lateinit var selectedRating: TextView

    private val movies = MovieRepository.movies

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        movieListContainer = findViewById(R.id.movieListContainer)
        selectedTitle = findViewById(R.id.selectedTitle)
        selectedMeta = findViewById(R.id.selectedMeta)
        selectedDescription = findViewById(R.id.selectedDescription)
        selectedPoster = findViewById(R.id.selectedPoster)
        selectedRating = findViewById(R.id.selectedRating)

        renderMovieCards()
        showMovieDetail(movies.first())
    }

    private fun renderMovieCards() {
        movieListContainer.removeAllViews()

        movies.forEachIndexed { index, movie ->
            val card = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                gravity = Gravity.CENTER
                isFocusable = true
                isFocusableInTouchMode = true
                background = getDrawable(R.drawable.movie_card_background)
                setPadding(22, 22, 22, 22)

                layoutParams = LinearLayout.LayoutParams(260, 360).apply {
                    setMargins(0, 0, 24, 0)
                }

                setOnFocusChangeListener { view, hasFocus ->
                    view.background = if (hasFocus) {
                        getDrawable(R.drawable.movie_card_focused_background)
                    } else {
                        getDrawable(R.drawable.movie_card_background)
                    }

                    if (hasFocus) {
                        showMovieDetail(movie)
                    }
                }

                setOnClickListener {
                    showMovieDetail(movie)
                }

                setOnKeyListener { _, keyCode, event ->
                    if (event.action == KeyEvent.ACTION_UP &&
                        (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER)
                    ) {
                        showMovieDetail(movie)
                        true
                    } else {
                        false
                    }
                }
            }

            val poster = TextView(this).apply {
                text = movie.posterSymbol
                textSize = 62f
                gravity = Gravity.CENTER
                setPadding(0, 8, 0, 10)
            }

            val title = TextView(this).apply {
                text = movie.title
                textSize = 18f
                setTextColor(getColor(R.color.white))
                typeface = Typeface.DEFAULT_BOLD
                gravity = Gravity.CENTER
                maxLines = 3
            }

            val year = TextView(this).apply {
                text = movie.year
                textSize = 15f
                setTextColor(getColor(R.color.mutedText))
                gravity = Gravity.CENTER
                setPadding(0, 10, 0, 0)
            }

            card.addView(poster)
            card.addView(title)
            card.addView(year)
            movieListContainer.addView(card)

            if (index == 0) {
                card.requestFocus()
            }
        }
    }

    private fun showMovieDetail(movie: Movie) {
        selectedPoster.text = movie.posterSymbol
        selectedTitle.text = movie.title
        selectedMeta.text = "${movie.year} • ${movie.genre} • ${movie.duration}"
        selectedRating.text = "⭐ ${movie.rating}/10"
        selectedDescription.text = movie.description
    }
}
""", encoding="utf-8")

# ----------------------------
# activity_main.xml
# ----------------------------
(RES_DIR / "layout/activity_main.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/rootLayout"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/appBackground"
    android:orientation="vertical"
    android:paddingStart="48dp"
    android:paddingTop="34dp"
    android:paddingEnd="48dp"
    android:paddingBottom="34dp">

    <TextView
        android:id="@+id/appTitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Movie TV"
        android:textColor="@color/white"
        android:textSize="34sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/appSubtitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="4dp"
        android:text="Browse favorite movies using a TV-style interface"
        android:textColor="@color/mutedText"
        android:textSize="16sp" />

    <LinearLayout
        android:id="@+id/contentLayout"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_marginTop="28dp"
        android:layout_weight="1"
        android:orientation="horizontal">

        <LinearLayout
            android:id="@+id/detailPanel"
            android:layout_width="0dp"
            android:layout_height="match_parent"
            android:layout_weight="1.1"
            android:background="@drawable/detail_panel_background"
            android:orientation="vertical"
            android:padding="32dp">

            <TextView
                android:id="@+id/selectedPoster"
                android:layout_width="match_parent"
                android:layout_height="120dp"
                android:gravity="center"
                android:text="🚀"
                android:textSize="72sp" />

            <TextView
                android:id="@+id/selectedTitle"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="16dp"
                android:text="Interstellar"
                android:textColor="@color/white"
                android:textSize="30sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/selectedMeta"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="10dp"
                android:text="2014 • Sci-Fi"
                android:textColor="@color/mutedText"
                android:textSize="16sp" />

            <TextView
                android:id="@+id/selectedRating"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginTop="18dp"
                android:background="@drawable/rating_background"
                android:paddingStart="16dp"
                android:paddingTop="8dp"
                android:paddingEnd="16dp"
                android:paddingBottom="8dp"
                android:text="⭐ 8.7/10"
                android:textColor="@color/white"
                android:textSize="16sp"
                android:textStyle="bold" />

            <TextView
                android:id="@+id/selectedDescription"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="24dp"
                android:lineSpacingExtra="6dp"
                android:text="Movie description"
                android:textColor="@color/white"
                android:textSize="18sp" />

            <TextView
                android:id="@+id/tvHint"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="28dp"
                android:text="Use remote / keyboard arrows to move between movies"
                android:textColor="@color/accent"
                android:textSize="15sp" />
        </LinearLayout>

        <HorizontalScrollView
            android:id="@+id/movieScroll"
            android:layout_width="0dp"
            android:layout_height="match_parent"
            android:layout_marginStart="28dp"
            android:layout_weight="1.7"
            android:fillViewport="true"
            android:scrollbars="none">

            <LinearLayout
                android:id="@+id/movieListContainer"
                android:layout_width="wrap_content"
                android:layout_height="match_parent"
                android:gravity="center_vertical"
                android:orientation="horizontal" />
        </HorizontalScrollView>
    </LinearLayout>
</LinearLayout>
""", encoding="utf-8")

# ----------------------------
# colors.xml
# ----------------------------
(RES_DIR / "values/colors.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="appBackground">#101827</color>
    <color name="panelBackground">#182235</color>
    <color name="cardBackground">#202D44</color>
    <color name="cardFocused">#E65C9B</color>
    <color name="accent">#FF8BC2</color>
    <color name="white">#FFFFFF</color>
    <color name="mutedText">#B8C2D6</color>
</resources>
""", encoding="utf-8")

# ----------------------------
# strings.xml
# ----------------------------
(RES_DIR / "values/strings.xml").write_text("""<resources>
    <string name="app_name">Movie TV</string>
</resources>
""", encoding="utf-8")

# ----------------------------
# themes.xml
# ----------------------------
(RES_DIR / "values/themes.xml").write_text("""<resources>
    <style name="Theme.TVAndroidApplication" parent="android:style/Theme.Material.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:windowFullscreen">false</item>
        <item name="android:statusBarColor">@color/appBackground</item>
        <item name="android:navigationBarColor">@color/appBackground</item>
        <item name="android:colorAccent">@color/accent</item>
    </style>
</resources>
""", encoding="utf-8")

# ----------------------------
# drawables
# ----------------------------
(RES_DIR / "drawable/movie_card_background.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/cardBackground" />
    <corners android:radius="24dp" />
    <stroke android:width="1dp" android:color="#34445F" />
</shape>
""", encoding="utf-8")

(RES_DIR / "drawable/movie_card_focused_background.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/cardFocused" />
    <corners android:radius="24dp" />
    <stroke android:width="4dp" android:color="@color/white" />
</shape>
""", encoding="utf-8")

(RES_DIR / "drawable/detail_panel_background.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/panelBackground" />
    <corners android:radius="28dp" />
</shape>
""", encoding="utf-8")

(RES_DIR / "drawable/rating_background.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#34445F" />
    <corners android:radius="40dp" />
</shape>
""", encoding="utf-8")

# ----------------------------
# AndroidManifest.xml
# ----------------------------
(APP_DIR / "src/main/AndroidManifest.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-feature
        android:name="android.hardware.touchscreen"
        android:required="false" />

    <uses-feature
        android:name="android.software.leanback"
        android:required="false" />

    <application
        android:allowBackup="true"
        android:banner="@mipmap/ic_launcher"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.TVAndroidApplication">

        <activity
            android:name="com.callmeshinny.tvandroidapplication.MainActivity"
            android:exported="true">

            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
            </intent-filter>

        </activity>
    </application>

</manifest>
""", encoding="utf-8")

# ----------------------------
# Patch build.gradle.kts
# ----------------------------
gradle_file = APP_DIR / "build.gradle.kts"
if gradle_file.exists():
    gradle_text = gradle_file.read_text(encoding="utf-8")
    gradle_text = re.sub(r'namespace\\s*=\\s*"[^"]+"', 'namespace = "com.callmeshinny.tvandroidapplication"', gradle_text)
    gradle_text = re.sub(r'applicationId\\s*=\\s*"[^"]+"', 'applicationId = "com.callmeshinny.tvandroidapplication"', gradle_text)
    gradle_file.write_text(gradle_text, encoding="utf-8")

# ----------------------------
# .gitignore
# ----------------------------
Path(".gitignore").write_text("""# Gradle
.gradle/
build/
*/build/

# Android Studio
.idea/
*.iml
local.properties

# OS files
.DS_Store
Thumbs.db

# Android build outputs
*.apk
*.ap_
*.aab
*.dex

# Native build
.externalNativeBuild/
.cxx/

# Captures
captures/

# Logs
*.log

# Signing / secrets
*.jks
*.keystore
keystore.properties
secrets.properties

# Generated release/debug folders
app/release/
app/debug/
""", encoding="utf-8")

# ----------------------------
# README.md
# ----------------------------
Path("README.md").write_text("\n".join(['# TV Android Movie Application - Mobile Development Lab 4', '', '## Student Information', '', '- **Full name:** Nguyễn Lê Như Ngọc', '- **Student ID:** 23521031', '- **Course:** Mobile Development', '- **Lab:** Lab 4', '- **Project name:** TV Android Movie Application', '', '## Project Overview', '', 'This project is a TV-style Android movie application developed for Lab 4 of the Mobile Development course.', '', 'The app displays a collection of favorite movies in a horizontal TV-style browsing interface. Users can move between movies using keyboard arrows, a TV remote, or emulator controls. When a movie is selected, the app displays its title, year, genre, duration, rating, and description.', '', '## Main Features', '', '- Display a list of favorite movies.', '- Browse movies using a horizontal TV-style layout.', '- Support D-pad / keyboard arrow navigation.', '- Highlight the focused movie card.', '- Show detailed movie information.', '- Display movie title, year, genre, duration, rating, and description.', '- Work offline with local movie data.', '- Support Android TV launcher through Leanback configuration.', '', '## Tech Stack', '', '- **Programming language:** Kotlin', '- **IDE:** Android Studio', '- **Platform:** Android / Android TV', '- **UI:** XML Layout and Kotlin dynamic views', '- **Build tool:** Gradle', '- **Architecture:** Simple local repository pattern', '', '## How the App Works', '', '1. The app loads a local movie list from MovieRepository.', '2. Movie cards are generated dynamically in MainActivity.', '3. Each movie card is focusable for TV remote or keyboard navigation.', '4. When a card receives focus, the detail panel updates automatically.', '5. The selected movie detail is shown on the left side of the screen.', '', '## How to Run', '', '1. Clone this repository:', '', 'https://github.com/callmeshinny/UIT_Mobile_Lab4_TVAndroidApplication_23521031', '', '2. Open the project in Android Studio.', '3. Wait for Gradle Sync to finish.', '4. Run the app on an emulator, Android device, or Android TV emulator.', '', 'Build from terminal:', '', './gradlew clean assembleDebug', '', 'Install on emulator or device:', '', './gradlew installDebug', '', '## Sample Movies', '', '- Interstellar', '- Spider-Man: Into the Spider-Verse', '- Inside Out', '- The Lion King', '- Coco', '- Avatar', '- Harry Potter and the Sorcerer Stone', '- Toy Story', '', '## Notes', '', 'This project uses local movie data, so it can work without internet access or an external API key.', '', '## Author', '', '**Nguyễn Lê Như Ngọc**  ', '**Student ID:** 23521031']) + "\n", encoding="utf-8")

print("Done: TV Android Movie App code, README, and .gitignore created successfully.")
