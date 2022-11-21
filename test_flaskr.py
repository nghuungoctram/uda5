import datetime
import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import setup_db

DATABASE_TEST_PATH = os.getenv('DATABASE_TEST_PATH')
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNod18yWWVPWFlrN1dPb1duZUF6NyJ9.eyJpc3MiOiJodHRwczovL2Rldi01ZXVlZ3E4NnFoZ2xxcno3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJlYWZUSDN1UGJYeDlxYnFnSTdwZlZDTFY3cjVYVFF6a0BjbGllbnRzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjY4Njc3ODEzLCJleHAiOjE2Njg3NjQyMTMsImF6cCI6ImVhZlRIM3VQYlh4OXFicWdJN3BmVkNMVjdyNVhUUXprIiwic2NvcGUiOiJwb3N0OnNoaXJ0IHBhdGNoOnNoaXJ0IGRlbGV0ZTpzaGlydCBwb3N0OmN1c3RvbWVyIHBhdGNoOmN1c3RvbWVyIGRlbGV0ZTpjdXN0b21lciIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInBvc3Q6c2hpcnQiLCJwYXRjaDpzaGlydCIsImRlbGV0ZTpzaGlydCIsInBvc3Q6Y3VzdG9tZXIiLCJwYXRjaDpjdXN0b21lciIsImRlbGV0ZTpjdXN0b21lciJdfQ.gtqPK_7XJBGrcgqsbawNxY8iP3Cg - \
    YhSG54Y55pQkGE48vM1CV6PlvbU8wnHuLtZwJhKwTdPitZAPlYkTzAiRfuy3D-TBNxkzh8OnmISEJgHXj5huaTWR5GiJpHLiVtYlxxTKp3lroRmamWqw6PQAYOJtfq3W6FV9n8eGZV_xR-In4_5NAy6G1 - \
    pI6yhij_H0UQXiHTep4hnTXYRExIMe-ZR9N77mmT6hICUcTYM4j_nGZ2oU3Kn9NjGD25J02 - \
    nFgdvSy9nlvvwQRXHy4DXBQVzRmhVkPVYSvC9DB4rOuOsJErR0eQmoCgjQeBvAWP3fd5yTbBfijk1NjhelLfm3A"


class testCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client
        self.database_path = DATABASE_TEST_PATH
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


# --------------------------------------------------
# SHIRT API
# --------------------------------------------------


    def test_get_shirts(self):
        res = self.client().get("/shirts")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        pass

    def test_new_shirt_method_fail(self):
        shirt = {
            "name": "hellow",
            "color": "red",
            "size": "S",
            "link": "http://1234"
        }
        res = self.client().post("/shirt", json=shirt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

        pass

    # test create new category pass with manage:categories permission
    def test_new_shirt_method_success(self):
        shirt = {
            "name": "hellow world",
            "color": "yello",
            "size": "L",
            "link": "http://hellow"
        }
        headers = {'Authorization': token}
        res = self.client().post("/shirt", json=shirt, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        pass

    # test update category fail with no token
    def test_update_shirt_fail(self):
        shirt = {
            "name": "123",
            "color": "pink",
            "size": "XXL",
            "link": "http://wrewrwegfdgdg"
        }

        res = self.client().patch("/shirt/0", json=shirt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

        pass

    # test update category fail if category doesn't exist
    def test_update_shirt_unvalid(self):
        shirt = {
            "name": "123 hellow",
            "color": "yellow pink",
            "size": "XXL",
            "link": "http://1111111111111"
        }

        headers = {'Authorization': token}
        res = self.client().delete("/shirt/1", json=shirt, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        pass

    # test delete category fail with no token
    def test_delete_shirt_fail(self):
        res = self.client().delete("/shirt/4")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

        pass

     # test delete category fail if category doesn't exist
    def test_update_shirt_not_exist(self):
        headers = {'Authorization': token}
        res = self.client().delete("/shirt/7", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        pass


# --------------------------------------------------
# CUSTOMER API
# --------------------------------------------------

    def test_get_customer(self):
        res = self.client().get("/customers")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        pass

    def test_new_customer_method_fail(self):
        customer = {
            "name": "111",
            "gender": "222",
            "phone": "333",
            "shirt_id": 0
        }
        res = self.client().post("/customer", json=customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

        pass

    # test create new category pass with manage:categories permission
    def test_new_customer_method_success(self):
        customer = {
            "name": "222",
            "gender": "111",
            "phone": "666",
            "shirt_id": 1
        }
        headers = {'Authorization': token}
        res = self.client().post("/customer", json=customer, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        pass

    # test update category fail with no token
    def test_update_customer_fail(self):
        customer = {
            "name": "4gfhf",
            "gender": "456456",
            "phone": "fghfh564",
            "shirt_id": 2
        }

        res = self.client().patch("/customer/2", json=customer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

        pass

    # test update category fail if category doesn't exist
    def test_update_customer_unvalid(self):
        customer = {
            "name": "hhh",
            "gender": "sss",
            "phone": "555",
            "shirt_id": 1
        }

        headers = {'Authorization': token}
        res = self.client().delete("/customer/1", json=customer, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        pass

    # test delete category fail with no token
    def test_delete_customer_fail(self):
        res = self.client().delete("/customer/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

        pass

     # test delete category fail if category doesn't exist
    def test_update_customer_not_exist(self):
        headers = {'Authorization': token}
        res = self.client().delete("/customer/6", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
