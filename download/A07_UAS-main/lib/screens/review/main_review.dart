import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class Review {
  final String restoranName;
  final String title;
  final String displayName;
  final double rating;
  final String reviewText;
  final String date;
  final List<String> images;
  final int likes;

  Review({
    required this.restoranName,
    required this.title,
    required this.displayName,
    required this.rating,
    required this.reviewText,
    required this.date,
    required this.images,
    required this.likes,
  });
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Main Review',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ReviewPage(),
    );
  }
}

class ReviewPage extends StatelessWidget {
  final List<Review> reviews = [
    Review(
      restoranName: "Restoran A",
      title: "Great food!",
      displayName: "John Doe",
      rating: 4.5,
      reviewText: "The food was amazing. I loved the ambiance.",
      date: "2024-11-28",
      images: ["https://via.placeholder.com/150", "https://via.placeholder.com/150"],
      likes: 10,
    ),
    // Add more reviews here
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reviews'),
        backgroundColor: Colors.black87,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.brown.withOpacity(0.7),
                  borderRadius: BorderRadius.circular(15),
                ),
                padding: EdgeInsets.all(20),
                child: Column(
                  children: [
                    Text(
                      'Reviews',
                      style: TextStyle(fontSize: 32, color: Colors.white),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Bagikan pengalaman Anda dengan restoran kami melalui ulasan!',
                      style: TextStyle(color: Colors.white70),
                    ),
                    SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.black87,
                      ),
                      child: Text('Tulis Ulasan'),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 20),
            Text(
              '──── Daftar Riwayat Ulasan ────',
              style: TextStyle(fontSize: 24, color: Colors.white),
            ),
            SizedBox(height: 10),
            GridView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 1,
                childAspectRatio: 2,
                mainAxisSpacing: 20,
              ),
              itemCount: reviews.length,
              itemBuilder: (context, index) {
                final review = reviews[index];
                return ReviewCard(review: review);
              },
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              child: Text('Kembali ke Restoran'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.brown),
            ),
          ],
        ),
      ),
    );
  }
}

class ReviewCard extends StatelessWidget {
  final Review review;

  const ReviewCard({Key? key, required this.review}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.brown.withOpacity(0.7),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              review.restoranName,
              style: TextStyle(fontSize: 22, color: Colors.white),
            ),
            Text(
              review.title,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white70),
            ),
            SizedBox(height: 8),
            Text(
              'Penulis: ${review.displayName}',
              style: TextStyle(color: Colors.white70),
            ),
            SizedBox(height: 8),
            Text(
              'Rating: ${review.rating} / 5',
              style: TextStyle(color: Colors.white),
            ),
            SizedBox(height: 8),
            Text(
              review.reviewText,
              style: TextStyle(color: Colors.white70),
            ),
            SizedBox(height: 8),
            Text(
              'Tanggal: ${review.date}',
              style: TextStyle(color: Colors.white70),
            ),
            SizedBox(height: 8),
            Wrap(
              children: review.images.map((image) {
                return Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: Image.network(
                    image,
                    width: 50,
                    height: 50,
                    fit: BoxFit.cover,
                  ),
                );
              }).toList(),
            ),
            SizedBox(height: 8),
            Row(
              children: [
                Icon(Icons.thumb_up, color: Colors.white),
                SizedBox(width: 5),
                Text(
                  '${review.likes} Like(s)',
                  style: TextStyle(color: Colors.white),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
