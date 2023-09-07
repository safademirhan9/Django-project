**Task**
odev_postman_collection adli dosya bir Postman Collection. Bunu Postman yazılımında import ettiğinde birkaç REST Web Service endpoint olduğunu göreceksin. Beklentimiz Django rest framework'ü kullanarak bu endpointleri çalıştırabilecek bir proje hazırlaman. Proje özünde havayolları ve onlara bağlı uçakların eklenebildiği, değiştirilebildiği ve listelenebildiği modüllerden ibaret. JWT Authentication kullanarak kullanıcının giriş yapıp yapmadığı kontrol edilecek.



**README**

- URL Cheatsheet: 

    List Airlines: http://localhost:8000/airline/list/

    Create Airline: http://localhost:8000/airline/
    Create Aircraft: http://localhost:8000/aircraft/

    Retrieve Airline: http://localhost:8000/airline/retrieve/2/
    Retrieve Aircraft: http://localhost:8000/aircraft/retrieve/2/

    Update Airline: http://localhost:8000/airline/update/2/
    Update Aircraft: http://localhost:8000/aircraft/update/2/

    Delete Airline: http://localhost:8000/airline/delete/2/
    Delete Aircraft: http://localhost:8000/aircraft/delete/2/

    Obtain Authentication Token: http://localhost:8000/api-token-auth/
    
    ** `2` burada airline_id veya aircraft_id yerine gecmektedir.
    



Program ile ilgili dikkat edilmesi gereken durumlar:
- Postman collection'daki URL pattern'ine uymaya calistim ancak,
    `create_airline` ve `list airline` icin verilen URL {{url}}/airline/
    ve farkli HTTP metotlari olsalar da, test etmeyi kolaylastirmasi adina
    `create_airline` icin URL'yi {{url}}/airline/ birakirken
    `list airline` icin URL'yi {{url}}/list_airlines/ yaptim.
    Benzer farkliliklari yukarda listeledim.

- create_airline, retrieve_aircraft gibi sayfalara giris yapmadan erisim
    engellenmistir, giris yapmaniz icin yonlendirilirsiniz.

- delete_airline ve delete_aircraft gibi fonksiyonlarda Postman'de import edildiginde
    URL pattern'ine {{url}}/airline/delete/{{airline_id}} uyarak yine de bir submit uyumlu template koydum. Yine de {{url}}/airline/delete/{{airline_id}} ile Postman uzerinden bu sayfaya erismeden de silme islemi yapabilmek mumkun.

- update_airline ve update_aircraft PATCH metotlari olduklarindan Postman uzerinden test edebildim ve "message": "Airline updated" donutunu alabildim.

- Authentication islevi istendigi gibi degilse geri donutunuz uzerine guncelleyebilirim.


