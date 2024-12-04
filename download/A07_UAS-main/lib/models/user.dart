class User {
  final int id;
  final String username;
  final String email;
  final String role;
  final String? token;

  User(
      {required this.id,
      required this.username,
      required this.email,
      required this.role,
      this.token});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
        id: json['id'],
        username: json['username'],
        email: json['email'],
        role: json['role'] == 'RESTO_OWNER' ? 'RESTO_OWNER' : 'CUSTOMER',
        token: json['token']);
  }
}
