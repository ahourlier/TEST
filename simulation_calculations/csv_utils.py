import csv

# Write headers
def write_csv_headers():
    write_log_in_csv(
        [
            "ID de projet",
            "Nom de simulation",
            "Total travaux TTC (OLD)",
            "Total travaux TTC (NEW)",
            "Total subventions (OLD)",
            "Total subventions (NEW)",
            "Reste à charge (OLD)",
            "Reste à charge (NEW)",
            "% \subvention sur le TTC (OLD)",
            "% \subvention sur le TTC (NEW)",
            "Total avances (OLD)",
            "Total avances (NEW)",
        ],
        append=False
    )

# Writing helper
def write_log_in_csv(row, append=True):
    with open("log_calculation.csv", "a" if append else "w+") as f:
        writer = csv.writer(f)
        writer.writerow(row)