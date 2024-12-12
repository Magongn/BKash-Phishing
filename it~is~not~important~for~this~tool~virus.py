#include <iostream>
#include <string>
#include <regex>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <openssl/sha.h> // Ensure you have OpenSSL installed

using namespace std;

// Function to hash the PIN using SHA256
string hashPin(const string& pin) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)pin.c_str(), pin.length(), hash);
    stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        ss << hex << setw(2) << setfill('0') << (int)hash[i];
    }
    return ss.str();
}

// Function to log the login information to a file
void logLoginInfo(const string& phoneNumber, const string& hashedPin) {
    ofstream file("login_info.txt", ios::app);
    if (file.is_open()) {
        time_t now = time(0);
        char* dt = ctime(&now);
        file << "Phone Number: " << phoneNumber << " | Hashed PIN: " << hashedPin << " | Timestamp: " << dt;
        file.close();
    } else {
        cerr << "Unable to open file for logging." << endl;
    }
}

// Function to validate the phone number and pin
bool isValid(const string& phoneNumber, const string& pin) {
    regex phoneRegex("\\d{11}");
    regex pinRegex("\\d{4,5}");
    return regex_match(phoneNumber, phoneRegex) && regex_match(pin, pinRegex);
}

int main() {
    string phoneNumber, pin;

    cout << "Enter Mobile Number: ";
    cin >> phoneNumber;

    cout << "Enter 4 or 5-digit PIN: ";
    cin >> pin;

    if (isValid(phoneNumber, pin)) {
        string hashedPin = hashPin(pin);
        logLoginInfo(phoneNumber, hashedPin);
        cout << "Login Successful!" << endl;
    } else {
        cerr << "Invalid phone number or PIN. Please try again." << endl;
    }

    return 0;
}  