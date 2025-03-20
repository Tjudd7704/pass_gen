import argparse
import zxcvbn
import statistics
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_password_statistics(input_file, ax, label):
    """
    Calculates statistics for zxcvbn scores of passwords in the input file.
    """
    with open(input_file, 'r', encoding="latin-1") as f:
        passwords = f.readlines()

    scores = []
    score_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for password in tqdm(passwords, desc=f"Calculating zxcvbn scores for {label}"):
        password = password.strip()
        if password:
            result = zxcvbn.zxcvbn(password)
            scores.append(result['score'])
            score_counts[result['score']] += 1

    mean_score = statistics.mean(scores)
    variance_score = statistics.variance(scores)
    median_score = statistics.median(scores)
    stdev_score = statistics.stdev(scores)

    print(f"{label}:")
    print(f"Number of passwords: {len(scores)}")
    print(f"Mean zxcvbn score: {mean_score}")
    print(f"Variance of zxcvbn scores: {variance_score}")
    print(f"Median zxcvbn score: {median_score}")
    print(f"Standard deviation of zxcvbn scores: {stdev_score}")
    for score, count in score_counts.items():
        strength = ["Very Weak", "Weak", "Fair", "Good", "Strong"][score]
        print(f"Score {score} ({strength}): {count}")

    sns.histplot(scores, bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], kde=False, ax=ax, label=label)
    ax.set_xticks(range(5))
    ax.set_xticklabels(["Very Weak", "Weak", "Fair", "Good", "Strong"])
    ax.set_xlabel("zxcvbn Strength Score")
    ax.set_ylabel("Number of Passwords")
    ax.set_title(f"Password Strength Distribution ({label})")
    ax.legend()

def calculate_unique_passwords(input_file, ax, label):
    """
    Calculates the number of unique passwords in the input file.
    """
    with open(input_file, 'r', encoding="latin-1") as f:
        passwords = f.readlines()

    passwords = [password.strip() for password in passwords]

    unique_passwords = len(set(passwords))
    duplicate_passwords = len(passwords) - unique_passwords

    ax.pie([unique_passwords, duplicate_passwords], labels=["Unique", "Duplicate"], autopct="%1.1f%%", colors=["green", "red"])
    ax.set_title(f"Uniqueness of Passwords ({label})")

def calculate_password_characteristics(input_file, ax, label):
    """
    Calculates statistics for password characteristics of passwords in the input file.
    """
    with open(input_file, 'r', encoding="latin-1") as f:
        passwords = f.readlines()

    passwords = [password.strip() for password in passwords]

    digit_count = sum(any(c.isdigit() for c in p) for p in passwords)
    upper_count = sum(any(c.isupper() for c in p) for p in passwords)
    special_count = sum(any(c in "!@#$%^&*()" for c in p) for p in passwords)

    # Grouped bar plot for better readability
    categories = ["Digits", "Uppercase", "Special"]
    counts = [digit_count, upper_count, special_count]
    ax.bar(categories, counts, label=label)
    ax.set_ylabel("Number of Passwords")
    ax.set_title(f"Character Type Distribution ({label})")
    ax.legend()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze generated passwords.")
    parser.add_argument("--input_files", nargs="+", type=str, help="Paths to the input files containing generated passwords")
    parser.add_argument("--labels", nargs="+", type=str, help="Labels for each input file")
    args = parser.parse_args()

    if len(args.input_files) != len(args.labels):
        raise ValueError("The number of input files and labels must be the same.")

    num_datasets = len(args.input_files)
    fig, axs = plt.subplots(3, num_datasets, figsize=(6 * num_datasets, 15))  # Adjust figure size

    for i, (input_file, label) in enumerate(zip(args.input_files, args.labels)):
        # Calculate and print statistics
        calculate_password_statistics(input_file, axs[0, i], label)

        # Calculate and print number of unique passwords
        calculate_unique_passwords(input_file, axs[1, i], label)

        # Calculate and print password characteristics
        calculate_password_characteristics(input_file, axs[2, i], label)

    plt.tight_layout(pad=4.0)  # Increase padding to prevent overlapping
    plt.show()
