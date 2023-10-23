from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks in seconds
    host = 'https://coherenceseo.onrender.com/'


    @task
    def check_indexing(self):
        # Define the URLs to test here
        urls = [
            "https://www.perionimmobilier.fr/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/compare-properties/",
            "https://www.perionimmobilier.fr/gerance-locative/"
        ]

        for url in urls:
            self.client.post('/check', data={'urls': url})

