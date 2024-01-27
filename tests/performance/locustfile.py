from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def home(self):
        self.client.get("/")

    @task
    def book_path(self):
        self.client.get("/book/Fall Classic/She Lifts")

    @task
    def purchase(self):
        response = self.client.post(
            "/purchasePlaces",
            {
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "1",
            },
        )
        if response.status_code == 400:
            print(
                "Received a 400 response code for the purchase task. It's because the club is unable to purchase places. Continuing..."
            )

    @task
    def table(self):
        self.client.get("/pointsDisplay")

    @task
    def login_and_logout(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})
        self.client.get("/logout")
