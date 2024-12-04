import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class AuthService {
  static const String baseUrl =
      'http://localhost:8000'; // Update to your server address
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  // Signup method
  Future<void> signUp({
    required String username,
    required String email,
    required String password1,
    required String password2,
    required String role,
  }) async {
    final url = Uri.parse('$baseUrl/auth/fsignup/');
    final body = {
      'username': username,
      'email': email,
      'password1': password1,
      'password2': password2,
      'role': role
    };

    try {
      final response =
          await http.post(url, headers: _jsonHeaders, body: jsonEncode(body));

      if (response.statusCode == 201) {
        return;
      } else if (response.statusCode == 400) {
        final errors = jsonDecode(response.body);
        throw AuthException(errors);
      } else {
        throw Exception('Unexpected error: ${response.statusCode}');
      }
    } catch (e) {
      rethrow;
    }
  }

  // Login method
  Future<void> login({
    required String username,
    required String password,
  }) async {
    final url = Uri.parse('$baseUrl/auth/flogin/');
    final body = {
      'username': username,
      'password': password,
    };

    try {
      final response =
          await http.post(url, headers: _jsonHeaders, body: jsonEncode(body));

      if (response.statusCode == 200) {
        await _storage.write(key: 'username', value: username);
        return;
      } else if (response.statusCode == 401) {
        throw AuthException({'detail': 'Invalid username or password'});
      } else {
        throw Exception('Unexpected error: ${response.statusCode}');
      }
    } catch (e) {
      rethrow;
    }
  }

  // Logout method
  Future<void> logout() async {
    final url = Uri.parse('$baseUrl/auth/flogout/');
    try {
      await http.post(url, headers: _jsonHeaders);
      await _storage.deleteAll(); // Clear stored credentials
    } catch (e) {
      throw Exception('Logout failed: $e');
    }
  }

  // Check if user is logged in
  Future<bool> isLoggedIn() async {
    return await _storage.read(key: 'username') != null;
  }

  // Common headers for JSON requests
  Map<String, String> get _jsonHeaders => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      };
}

// Custom exception for handling form errors
class AuthException implements Exception {
  final Map<String, dynamic> errors;

  AuthException(this.errors);

  @override
  String toString() => errors.toString();
}
