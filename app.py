from shiny import App, render, ui
import pandas as pd
import matplotlib.pyplot as plt

# Sample data structure
df = pd.read_csv("data/release_data.csv")

app_ui = ui.page_fluid(
    ui.card(
        ui.card_header("Summary"),
        ui.output_table("summary_table")
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Genres"),
            ui.output_plot("genre_plot")
        ),
        ui.card(
            ui.card_header("Formats"),
            ui.output_plot("format_plot")
        ),
    )
)

def server(input, output, session):
    def create_bar_plot(data, column):
        plt.figure(figsize=(8, 4))
        counts = data[column].value_counts()
        plt.bar(counts.index, counts.values)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Count')
        plt.tight_layout()

    @output
    @render.table
    def summary_table():
        genre_counts = df['genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        format_counts = df['format'].value_counts().reset_index()
        format_counts.columns = ['Format', 'Count']
        
        # Combine both counts side by side
        max_len = max(len(genre_counts), len(format_counts))
        genre_counts = genre_counts.reindex(range(max_len))
        format_counts = format_counts.reindex(range(max_len))
        
        return pd.concat([genre_counts, format_counts], axis=1)

    @output
    @render.plot
    def genre_plot():
        create_bar_plot(df, 'genre')

    @output
    @render.plot
    def format_plot():
        create_bar_plot(df, 'format')

app = App(app_ui, server)