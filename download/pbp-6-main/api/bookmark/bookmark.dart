import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class BookmarkPage extends StatefulWidget {
  const BookmarkPage({Key? key}) : super(key: key);

  @override
  State<BookmarkPage> createState() => _BookmarkPageState();
}

class _BookmarkPageState extends State<BookmarkPage> {
  List bookmarks = [];

  @override
  void initState() {
    super.initState();
    fetchBookmarks();
  }

  Future<void> fetchBookmarks() async {
    final request = context.watch<CookieRequest>(); // Ambil instance CookieRequest
    final url = 'https://127.0.0.1:8000/bookmark'; // Endpoint Django bookmark_list

    final response = await request.get(url);

    if (response.statusCode == 200) {
      setState(() {
        bookmarks = jsonDecode(response.body);
      });
    } else {
      print('Failed to fetch bookmarks: ${response.body}');
    }
  }

  Future<void> toggleBookmark(int restaurantId) async {
    final request = context.watch<CookieRequest>();
    final url = 'https://127.0.0.1:8000/bookmark';

    final response = await request.post(url, {});

    if (response['status'] == true) {
      fetchBookmarks(); // Refresh daftar bookmark
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(response['message'])),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Gagal memperbarui bookmark: ${response['message']}')),
      );
    }
  }

  Future<void> deleteBookmark(int bookmarkId) async {
    final url =
        Uri.parse('https://example.com/bookmarks/delete/$bookmarkId/'); // URL API delete_bookmark
    final response = await http.delete(url, headers: {
      'Authorization': 'Bearer <your_token>', // Ganti dengan token autentikasi
    });

    if (response.statusCode == 200) {
      fetchBookmarks(); // Refresh daftar bookmark setelah penghapusan
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Bookmark berhasil dihapus")),
      );
    } else {
      print('Failed to delete bookmark: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Daftar Restoran Favorit Saya"),
        backgroundColor: const Color(0xFF795548), // Warna coklat sesuai desain
      ),
      body: bookmarks.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: bookmarks.length,
              itemBuilder: (context, index) {
                final bookmark = bookmarks[index];
                return Card(
                  color: const Color(0xFFD7CCC8), // Warna sesuai desain
                  margin: const EdgeInsets.only(bottom: 16.0),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          bookmark['restaurant']['name'], // Nama restoran
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          "Disimpan pada tanggal ${bookmark['date_added']}",
                          style: const TextStyle(fontSize: 14),
                        ),
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            ElevatedButton(
                              onPressed: () {
                                // Navigasi ke halaman restoran
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.white,
                                foregroundColor: const Color(0xFF795548),
                                side: const BorderSide(
                                  color: Color(0xFF795548),
                                ),
                              ),
                              child: const Text("View"),
                            ),
                            ElevatedButton(
                              onPressed: () {
                                deleteBookmark(bookmark['id']);
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.white,
                                foregroundColor: const Color(0xFF795548),
                                side: const BorderSide(
                                  color: Color(0xFF795548),
                                ),
                              ),
                              child: const Text("Remove"),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
