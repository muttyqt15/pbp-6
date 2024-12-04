import 'dart:convert';

List<Review> reviewFromJson(String str) => List<Review>.from(json.decode(str).map((x) => Review.fromJson(x)));

String reviewToJson(List<Review> data) => json.encode(List<dynamic>.from(data.map((x) => x.toJson())));

class Review {
    String model;
    String pk;
    Fields fields;

    Review({
        required this.model,
        required this.pk,
        required this.fields,
    });

    factory Review.fromJson(Map<String, dynamic> json) => Review(
        model: json["model"],
        pk: json["pk"],
        fields: Fields.fromJson(json["fields"]),
    );

    Map<String, dynamic> toJson() => {
        "model": model,
        "pk": pk,
        "fields": fields.toJson(),
    };
}

class Fields {
    int customer;
    int restoran;
    String judulUlasan;
    DateTime tanggal;
    String teksUlasan;
    int penilaian;
    DateTime waktuEditTerakhir;
    String displayName;
    List<int> likes;

    Fields({
        required this.customer,
        required this.restoran,
        required this.judulUlasan,
        required this.tanggal,
        required this.teksUlasan,
        required this.penilaian,
        required this.waktuEditTerakhir,
        required this.displayName,
        required this.likes,
    });

    factory Fields.fromJson(Map<String, dynamic> json) => Fields(
        customer: json["customer"],
        restoran: json["restoran"],
        judulUlasan: json["judul_ulasan"],
        tanggal: DateTime.parse(json["tanggal"]),
        teksUlasan: json["teks_ulasan"],
        penilaian: json["penilaian"],
        waktuEditTerakhir: DateTime.parse(json["waktu_edit_terakhir"]),
        displayName: json["display_name"],
        likes: List<int>.from(json["likes"].map((x) => x)),
    );

    Map<String, dynamic> toJson() => {
        "customer": customer,
        "restoran": restoran,
        "judul_ulasan": judulUlasan,
        "tanggal": "${tanggal.year.toString().padLeft(4, '0')}-${tanggal.month.toString().padLeft(2, '0')}-${tanggal.day.toString().padLeft(2, '0')}",
        "teks_ulasan": teksUlasan,
        "penilaian": penilaian,
        "waktu_edit_terakhir": waktuEditTerakhir.toIso8601String(),
        "display_name": displayName,
        "likes": List<dynamic>.from(likes.map((x) => x)),
    };
}
