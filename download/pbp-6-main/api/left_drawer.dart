import 'package:flutter/material.dart';
import 'package:uas/screens/landing.dart'; 
import 'package:uas/screens/authentication/login.dart'
import 'package:uas/screens/authentication/register.dart'

class LeftDrawer extends StatelessWidget {
  final bool isLoggedIn; // Parameter untuk menentukan status login
  final String? userName; // Nama pengguna jika login
  final String? userRole; // Role pengguna jika login

  const LeftDrawer({
    Key? key,
    required this.isLoggedIn,
    this.userName,
    this.userRole,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          // Header
          DrawerHeader(
            decoration: const BoxDecoration(
              color: Color(0xFF795548), // Warna coklat sesuai desain
            ),
            child: isLoggedIn
                ? Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const CircleAvatar(
                            backgroundColor: Colors.white,
                            child: Icon(Icons.person, color: Colors.brown),
                          ),
                          const SizedBox(width: 16),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                userName ?? "Guest",
                                style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                              ),
                              Text(
                                userRole ?? "Customer",
                                style: const TextStyle(
                                  fontSize: 14,
                                  color: Colors.white70,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  )
                : const Center(
                    child: Text(
                      "MANGAN\" SOLO",
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
          ),

          // Menu Items
          ListTile(
            leading: const Icon(Icons.restaurant_menu),
            title: const Text('Homepage'),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (context) => LandingPage(),
                  ));
            },
          ),
          ListTile(
            leading: const Icon(Icons.restaurant_menu),
            title: const Text('Restoran'),
            onTap: () {
              Navigator.pop(context);
              // Navigasi ke halaman restoran
            },
          ),
          ListTile(
            leading: const Icon(Icons.forum),
            title: const Text('Thread'),
            onTap: () {
              Navigator.pop(context);
              // Navigasi ke halaman thread
            },
          ),
          ListTile(
            leading: const Icon(Icons.article_outlined),
            title: const Text('Berita'),
            onTap: () {
              Navigator.pop(context);
              // Navigasi ke halaman berita
            },
          ),
          ListTile(
            leading: const Icon(Icons.bookmark_border),
            title: const Text('Bookmark'),
            onTap: () {
              Navigator.pop(context);
              // Navigasi ke halaman bookmark
            },
          ),

          // Footer
          const Divider(),
          if (isLoggedIn)
            ListTile(
                    leading: const Icon(Icons.logout),
                    title: const Text('Logout'),
                    onTap: () async {
                      final response = await request.logout(
                          "http://127.0.0.1:8000/logout-flutter/");
                      String message = response["message"];
                      if (context.mounted) {
                        if (response['status']) {
                          String uname = response["username"];
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text("$message Goodbye, $uname!"),
                            ),
                          );
                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const LandingPage(),
                            ),
                          );
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(message),
                            ),
                          );
                        }
                      }
                    },
                  ),
          else ...[
            ListTile(
              leading: const Icon(Icons.person_add),
              title: const Text('Register'),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const RegisterPage(),
                        ),
                ),
              },
            ),
            ListTile(
              leading: const Icon(Icons.login),
              title: const Text('Login'),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const LoginPage(),
                        ),
                ),
              },
            ),
          ],
        ],
      ),
    );
  }
}
