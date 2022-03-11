import csv

# Write headers
def write_csv_headers():
    write_log_in_csv(
        [
            "ID de projet",
            "Nom de simulation",
            "Total travaux TTC",
            "Total subventions",
            "Reste à charge",
            "% \subvention sur le TTC",
            "Total avances",
        ],
        append=False
    )

# Writing helper
def write_log_in_csv(row, append=True):
    with open("log_calculation.csv", "a" if append else "w+") as f:
        writer = csv.writer(f)
        writer.writerow(row)