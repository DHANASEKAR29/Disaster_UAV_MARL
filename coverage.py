class CoverageMap:

    def __init__(self, size):

        self.size = size
        self.covered = set()

    # -----------------------------
    # Mark visited cell
    # -----------------------------
    def mark(self, x, y):

        if 0 <= x < self.size and 0 <= y < self.size:
            self.covered.add((x, y))

    # -----------------------------
    # Total covered cells
    # -----------------------------
    def total_covered(self):

        return len(self.covered)

    # -----------------------------
    # Coverage Percentage
    # -----------------------------
    def percentage(self):

        total_cells = self.size * self.size

        return (len(self.covered) / total_cells) * 100

    # -----------------------------
    # Used by main.py
    # -----------------------------
    def get_coverage_percentage(self):

        return self.percentage()

    # -----------------------------
    # Reset Coverage
    # -----------------------------
    def reset(self):

        self.covered.clear()

    # -----------------------------
    # Display Coverage Map
    # -----------------------------
    def display(self):

        print("\n========= COVERAGE MAP =========")

        for i in range(self.size):

            row = []

            for j in range(self.size):

                if (i, j) in self.covered:
                    row.append("V")
                else:
                    row.append(".")

            print(" ".join(row))

        print("\nCovered Cells :", self.total_covered())
        print(f"Coverage      : {self.percentage():.2f}%")