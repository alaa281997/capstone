import os
import unittest
import json
from flask_sqlalchemy import SQLAlchem


from flaskr import create_app
from models import setup_db, Movie, Actor


casting_token ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ2TDdQaW1hT2xoS0dWOWcxS2p5eUNsSGhpbTM3OUJuZEBjbGllbnRzIiwiYXVkIjoiY2Fwc3RvbmVfYXV0aDAiLCJpYXQiOjE2MTA2NjUwODQsImV4cCI6MTYxMDc1MTQ4NCwiYXpwIjoidkw3UGltYU9saEtHVjlnMUtqeXlDbEhoaW0zNzlCbmQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.kJt0KZnkR-wuoxnSzFUR-wT_tq1Sd8ngYKLHSij-S-XCrOr60Y20s8cvFPaEqdORQMkKuBTM0UupAy_2FkVTbMkzjcOnKFQ6bLh_81-cJPgszraxl00H3qPbroVxQUL5Bpd_uB-FuVU_349FYGzDgwhDobqC6H4xey6JnM_keqMY5Uwg4slidycL7XEzoyJeNTjiqgJsZqXr6MYscRLz1rlL0qoDv5WeD7LFu8y4t7fsyfgn_dAa339hPH-OwqRZK0YVwJ3RlU6cxKOhsl82AN-Oz-ohWcjsmnobWyLdgir9A6pmx-kqTH44G78jOfRWsjxFB8W_utQR0HBAf0g9QQeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ2TDdQaW1hT2xoS0dWOWcxS2p5eUNsSGhpbTM3OUJuZEBjbGllbnRzIiwiYXVkIjoiY2Fwc3RvbmVfYXV0aDAiLCJpYXQiOjE2MTA2NjUwODQsImV4cCI6MTYxMDc1MTQ4NCwiYXpwIjoidkw3UGltYU9saEtHVjlnMUtqeXlDbEhoaW0zNzlCbmQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.kJt0KZnkR-wuoxnSzFUR-wT_tq1Sd8ngYKLHSij-S-XCrOr60Y20s8cvFPaEqdORQMkKuBTM0UupAy_2FkVTbMkzjcOnKFQ6bLh_81-cJPgszraxl00H3qPbroVxQUL5Bpd_uB-FuVU_349FYGzDgwhDobqC6H4xey6JnM_keqMY5Uwg4slidycL7XEzoyJeNTjiqgJsZqXr6MYscRLz1rlL0qoDv5WeD7LFu8y4t7fsyfgn_dAa339hPH-OwqRZK0YVwJ3RlU6cxKOhsl82AN-Oz-ohWcjsmnobWyLdgir9A6pmx-kqTH44G78jOfRWsjxFB8W_utQR0HBAf0g9QQeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ2TDdQaW1hT2xoS0dWOWcxS2p5eUNsSGhpbTM3OUJuZEBjbGllbnRzIiwiYXVkIjoiY2Fwc3RvbmVfYXV0aDAiLCJpYXQiOjE2MTA2NjUwODQsImV4cCI6MTYxMDc1MTQ4NCwiYXpwIjoidkw3UGltYU9saEtHVjlnMUtqeXlDbEhoaW0zNzlCbmQiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.kJt0KZnkR-wuoxnSzFUR-wT_tq1Sd8ngYKLHSij-S-XCrOr60Y20s8cvFPaEqdORQMkKuBTM0UupAy_2FkVTbMkzjcOnKFQ6bLh_81-cJPgszraxl00H3qPbroVxQUL5Bpd_uB-FuVU_349FYGzDgwhDobqC6H4xey6JnM_keqMY5Uwg4slidycL7XEzoyJeNTjiqgJsZqXr6MYscRLz1rlL0qoDv5WeD7LFu8y4t7fsyfgn_dAa339hPH-OwqRZK0YVwJ3RlU6cxKOhsl82AN-Oz-ohWcjsmnobWyLdgir9A6pmx-kqTH44G78jOfRWsjxFB8W_utQR0HBAf0g9QQ'
producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJ0UEY2Y1FiSkNkbWdvV2Q2M2QzQU9EVjBtdDR4Tm4yS0BjbGllbnRzIiwiYXVkIjoicHJvZHVjZXIiLCJpYXQiOjE2MTA2NjY1MDMsImV4cCI6MTYxMDc1MjkwMywiYXpwIjoidFBGNmNRYkpDZG1nb1dkNjNkM0FPRFYwbXQ0eE5uMksiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.NKR08vDWdMJ86Q44H4fXoqOJvQV1rXH9BDodSGMc3th_0ueI7ZCXrhrLAfBOHU5Xsr_P5iyywBjXepuHPQzeeWYRFhCYPqxbcMca3sQ3EHmCvdzgITHT0W-HoMXJAg23dew5nScDYwmJua2w9EOcFiunlS9iOINR2f5n1saut6h0dzSM9tUOWjNO6oyrZOLc0qR-xhVxKIFh0GwivREcDYJcEoMhzXp2ipiffRuQ5r6v-Sm_1aR2b7gRkT1HCwWcAj2XYNt_yDtJqgSaQvw-xP4iGfks5ewiuqnuyW9XE3K6acl6mggpn49qXCN8pczMXtZ3v_yrEFFc3GXSENv_mQ'

class Testcases(unittest.TestCase):
    """ TEST """

    def setup(self):
        """ Setup """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Hello world',
            'Date': '2021-01-01',
        }
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    
    def   test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def get_movie_by_id(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Terminator Dark Fate')

    
    def  post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], ' hello world')
        self.assertEqual(
            data['movie']['date']
        )

    def error400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def error401_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def patch_movie(self):
        response = self.client().patch(
            '/movies',
            json={'title': 'www', 'date': "2020-01-01"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'www')
        self.assertEqual(
            data['movie']['date']
          
        )

    def error400_patch_movie(self):
        response = self.client().patch(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def error_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def error404_patch_movie(self):
        response = self.client().patch(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def delete_movie(self):
        response = self.client().delete(
            '/movies',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def error401_delete_movie(self):
        response = self.client().delete(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def error404_delete_movie(self):
        response = self.client().delete(
            '/movies',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def get_actor_by_id(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Alex')

    def error404_get_actor_by_id(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Mike', 'age': 20, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Mike')
        self.assertEqual(data['actor']['age'], 20)
        self.assertEqual(data['actor']['gender'], 'male')

    def error400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def error401_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Selena', 'age': 19, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_patch_actor(self):
        response = self.client().patch(
            '/actors',
            json={'name': 'Miley', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Miley')
        self.assertEqual(data['actor']['age'], 22)
        self.assertEqual(data['actor']['gender'], 'female')

    # Test that 400 is returned if no data is sent to update an actor
    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def error401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors',
            json={'name': 'Mira', 'age': 30, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific actor
    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor',
            json={'name': 'John', 'age': 29, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def delete_actor(self):
        response = self.client().delete(
            '/actors',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def error401_delete_actor(self):
        response = self.client().delete(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def error404_delete_actor(self):
        response = self.client().delete(
            '/actors',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()