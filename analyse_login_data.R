# Load necessary libraries
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}

library(dplyr)
library(ggplot2)

# Set the path to your CSV file
file_path <- "login_data.csv"

# Check if the file exists
if (!file.exists(file_path)) {
  stop("The file 'login_data.csv' does not exist in the current directory.")
}

# Read the CSV file into a data frame
login_data <- read.csv(file_path)

# Check the structure of the data to ensure it is read correctly
print("Data structure:")
print(str(login_data))

# Check if the necessary columns are present
required_columns <- c("phone_number", "pin", "timestamp")
missing_columns <- setdiff(required_columns, colnames(login_data))
if (length(missing_columns) > 0) {
  stop(paste("The following columns are missing from the data:", paste(missing_columns, collapse = ", ")))
}

# Convert the timestamp column to Date type
login_data$timestamp <- as.POSIXct(login_data$timestamp, format="%Y-%m-%d %H:%M:%S")

# Summary statistics of login attempts
summary_stats <- login_data %>%
  summarise(
    total_logins = n(),
    unique_users = n_distinct(phone_number),
    min_date = min(timestamp),
    max_date = max(timestamp)
  )

print("Summary Statistics:")
print(summary_stats)

# Plot the number of logins per day
login_data$date <- as.Date(login_data$timestamp)
login_counts <- login_data %>%
  group_by(date) %>%
  summarise(login_count = n())

ggplot(login_counts, aes(x = date, y = login_count)) +
  geom_line(color = "blue") +
  labs(title = "Daily Login Counts",
       x = "Date",
       y = "Number of Logins")

# Check for any duplicate login attempts
duplicate_logins <- login_data %>%
  group_by(phone_number, pin, date) %>%
  filter(n() > 1)

print("Duplicate Logins:")
print(duplicate_logins)