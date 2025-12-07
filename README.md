# Music Stats for Spotify

A Python toolkit to analyze and visualize your Extended Streaming History from Spotify.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amzoeee/musicstats_spotify.git
    cd musicstats_spotify
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Request Data**: Download your "Extended Streaming History" from Spotify Privacy Settings.
2.  **Add Data**: Place the JSON files (e.g., `Streaming_History_Audio_2023-2024.json`) into the `data/` directory.
3.  **Run Processing**:
    ```bash
    python main.py
    ```
    This will process your history and generate summary files in `output/txt/` and CSVs in `output/csv/`.

4.  **Visualize**: Run any of the plotting scripts in `src/plotting/` to see graphs.

## Output Structure

-   `data/`: Place your raw Spotify input files here.
-   `output/`:
    -   `csv/`: Processed data files (`tracks.csv`, `artists.csv`).
    -   `txt/`: Human-readable summaries.

## Scripts

### Processing
-   `main.py`: The main entry point. Orchestrates sorting and cleaning.
-   `src/processing/sort_track.py`: Aggregates data by track.
-   `src/processing/sort_artist.py`: Aggregates data by artist.
-   `src/processing/clean.py`: Generates human-readable text reports.

### Visualization (`src/plotting/`)
-   `all_plays.py`: Scatter plot of all listening history over time.
-   `graphtopn_playcount.py` / `graphtopn_playtime.py`: Bar charts of top artists and tracks.
-   `graphartists_*.py`: Various charts for artist statistics (playtime, playcount, unique tracks).
-   `graphtracks_*.py`: Various charts for track statistics.


