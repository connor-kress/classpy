import requests
from requests.auth import HTTPBasicAuth
import json
import os
from typing import List, Dict, Optional


class Professor:
    """Class representing a RateMyProfessors professor."""

    def __init__(self, name, _id, legacy_id, avg_rating, num_ratings, would_take_again_percent, avg_difficulty,
                 department, ratings):
        """Initialize a Professor object with the provided data."""
        self.name = name
        self.id = _id
        self.legacy_id = legacy_id
        self.avg_rating = avg_rating
        self.num_ratings = num_ratings
        self.would_take_again_percent = would_take_again_percent
        self.avg_difficulty = avg_difficulty
        self.department = department
        self.ratings = ratings

    def to_dict(self) -> Dict:
        """Convert Professor object to a dictionary."""
        return {
            "name": self.name,
            "id": self.id,
            "legacyId": self.legacy_id,
            "avgRating": self.avg_rating,
            "numRatings": self.num_ratings,
            "wouldTakeAgainPercent": self.would_take_again_percent,
            "avgDifficulty": self.avg_difficulty,
            "department": self.department,
            "ratings": self.ratings
        }

    @classmethod
    def from_dict(cls, professor_dict: Dict) -> 'Professor':
        """Create a Professor object from a dictionary."""
        return cls(
            professor_dict["name"],
            professor_dict["id"],
            professor_dict["legacyId"],
            professor_dict["avgRating"],
            professor_dict["numRatings"],
            professor_dict["wouldTakeAgainPercent"],
            professor_dict["avgDifficulty"],
            professor_dict["department"],
            professor_dict["ratings"]
        )

    def __str__(self) -> str:
        """Convert Professor object to a formatted string."""
        course_review = self.ratings.get("CourseReview", "")
        course_review_str = f"""
        Course Review:
            Course: {course_review.get("Course", "")}
            Comment: {course_review.get("Comment", "")}
            Date: {course_review.get("Date", "")}
            Grade: {course_review.get("Grade", "")}
            Online Class: {course_review.get("Online Class", "")}
            Rating Tags: {course_review.get("Rating Tags", "")}
            Textbook Used: {course_review.get("Textbook Used", "")}
            Attendance: {course_review.get("Attendance", "")}
        """ if course_review else ""

        return f"""Professor: {self.name} 
            Rating: {self.avg_rating}
            Number of Ratings: {self.num_ratings}
            Percent Would Take Again: {self.would_take_again_percent},
            Difficulty Rating: {self.avg_difficulty}
            Department: {self.department}
            {course_review_str}
            """


class RateMyProfessorsScraper:
    """Class for scraping RateMyProfessors data."""

    def __init__(self, school_id: str, filename: str = 'rmp.json'):
        """Initialize the scraper with school ID and optional filename."""
        self.auth_session = self.create_session("test", "test")
        self.school_id = school_id
        self.filename = filename

    def load_or_create_json(self) -> Optional[List[Professor]]:
        """Load existing data from a JSON file or create an empty list."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                professors = [Professor.from_dict(prof_dict) for prof_dict in data]
                return professors
        else:
            return None

    def create_session(self, username: str, password: str) -> requests.Session:
        """Create and return an authenticated HTTP session."""
        auth = HTTPBasicAuth(username, password)
        session = requests.Session()
        session.auth = auth
        return session

    def construct_query(self, cursor: str, page_size: int) -> str:
        """Construct a GraphQL query for RateMyProfessors."""
        return f"""
        {{
          newSearch {{
            teachers(after: "{cursor}", first: {page_size}, query: {{ fallback: true, schoolID: "{self.school_id}", text: "" }}) {{
              pageInfo {{
                hasNextPage
                endCursor
              }}
              edges {{
                node {{
                  id
                  legacyId
                  firstName
                  lastName
                  avgRating
                  numRatings
                  wouldTakeAgainPercent
                  avgDifficulty
                  department
                  ratings {{
                    edges {{
                      node {{
                        attendanceMandatory
                        class
                        comment
                        date
                        grade
                        isForOnlineClass
                        ratingTags
                        textbookUse
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """

    def process_teachers(self, teachers: List[Dict]) -> List[Professor]:
        """Process teacher data from RateMyProfessors."""
        processed_professors = []

        for teacher in teachers:
            teacher_node = teacher.get("node", {})
            num_ratings = teacher_node.get("numRatings", 0)

            ratings_edges = teacher_node.get("ratings", {}).get("edges", [])
            teacher_name = teacher_node.get("firstName", "") + " " + teacher_node.get("lastName", "")
            professor_data = {
                "name": teacher_name,
                "id": teacher_node.get("id", ""),
                "legacyId": teacher_node.get("legacyId", ""),
                "avgRating": teacher_node.get("avgRating", ""),
                "numRatings": num_ratings,
                "wouldTakeAgainPercent": teacher_node.get("wouldTakeAgainPercent", "")
                if teacher_node.get("wouldTakeAgainPercent", "") != -1 else "N/A",
                "avgDifficulty": teacher_node.get("avgDifficulty", ""),
                "department": teacher_node.get("department", ""),
            }

            most_recent_reviews = {}
            textbook_use_mapping = {
                -1: "N/A",
                0: "No",
                2: "No",
                3: "Yes",
                4: "Yes",
                5: "Yes",
            }
            is_online_mapping = {
                False: "No",
                True: "Yes"
            }
            attendance_mandatory_mapping = {
                "Y": "Mandatory",
                "N": "Not Mandatory"
            }

            for rating_edge in ratings_edges:
                rating_node = rating_edge.get("node", {})
                class_name = rating_node.get("class", "")

                if class_name not in most_recent_reviews or rating_node.get("date", "") > most_recent_reviews[
                    class_name].get(
                        "date", ""):
                    most_recent_reviews[class_name] = {
                        "attendanceMandatory": attendance_mandatory_mapping.get(
                            rating_node.get("attendanceMandatory", None),
                            None),
                        "comment": rating_node.get("comment", ""),
                        "date": rating_node.get("date", ""),
                        "grade": rating_node.get("grade", ""),
                        "isForOnlineClass": is_online_mapping.get(rating_node.get("isForOnlineClass", None), None),
                        "ratingTags": rating_node.get("ratingTags", ""),
                        "textbookUse": textbook_use_mapping.get(rating_node.get("textbookUse", None), None)
                    }

            professor = Professor(
                name=professor_data["name"],
                _id=professor_data["id"],
                legacy_id=professor_data["legacyId"],
                avg_rating=professor_data["avgRating"],
                num_ratings=professor_data["numRatings"],
                would_take_again_percent=professor_data["wouldTakeAgainPercent"],
                avg_difficulty=professor_data["avgDifficulty"],
                department=professor_data["department"],
                ratings=most_recent_reviews
            )

            processed_professors.append(professor)

        return processed_professors

    def make_request(self, endpoint: str, headers: Dict[str, str], payload: Dict) -> Dict:
        """Make a POST request to RateMyProfessors GraphQL endpoint."""
        response = self.auth_session.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def save_to_json(self, data: List[Professor]) -> None:
        """Save a list of Professor objects to a JSON file."""
        converted_data = [professor.to_dict() for professor in data]
        with open(self.filename, 'w') as f:
            json.dump(converted_data, f, indent=4)

    def get_professors_by_course(self, data: List[Professor], course_name: str) -> List[Professor]:
        """Get professors who have ratings for the specified course."""
        professors_for_course = []

        for professor in data:
            ratings = professor.ratings

            if course_name in ratings:
                professors_for_course.append(professor)

        return professors_for_course

    def get_professor_by_name(self, data: List[Professor], full_name: str) -> Optional[Professor]:
        """Get a professor by full name."""
        for professor in data:
            if professor.name == full_name:
                return professor

        return None

    def get_professor_by_name_and_course(self, data: List[Professor], full_name: str, course_name: str) -> Optional[
        Professor]:
        """Get a professor with course review by name and course."""
        for professor in data:
            if professor.name == full_name:
                ratings = professor.ratings.get(course_name)

                if ratings:
                    professor.ratings["CourseReview"] = {
                        "Course": course_name,
                        "Comment": ratings.get("comment", ""),
                        "Date": ratings.get("date", ""),
                        "Grade": ratings.get("grade", None),
                        "Online Class": ratings.get("isForOnlineClass", False),
                        "Rating Tags": ratings.get("ratingTags", None),
                        "Textbook Used": ratings.get("textbookUse", None),
                        "Attendance": ratings.get("attendanceMandatory", None)
                    }

                    return professor

        return None

    def get_course_reviews(self, data: List[Professor], course_name: str) -> str:
        reviews = []

        for professor in data:
            ratings = professor.ratings.get(course_name, {})  # Get ratings for the specified course

            if not ratings:
                continue  # Skip professors without ratings for the specified course

            # Format the review data as a string
            review_str = f"""
                Course Review:
                    Course: {course_name}
                    Comment: {ratings.get("comment", "")}
                    Date: {ratings.get("date", "")}
                    Grade: {ratings.get("grade", "N/A")}
                    Online Class: {ratings.get("isForOnlineClass", False)}
                    Rating Tags: {ratings.get("ratingTags", "")}
                    Textbook Used: {ratings.get("textbookUse", "N/A")}
                    Attendance: {ratings.get("attendanceMandatory", "N/A")}
                """

            reviews.append(review_str)

        return "\n".join(reviews)

    def scrape_data(self) -> None:
        """Scrape RateMyProfessors data and save it to a JSON file."""
        existing_data = self.load_or_create_json()

        if existing_data is not None:
            all_results = existing_data
        else:
            all_results = []
            cursor = ""
            has_next_page = True
            page_size = 1000
            headers = {"Content-Type": "application/json"}

            while has_next_page:
                graphql_query = self.construct_query(cursor, page_size)
                payload = {"query": graphql_query}
                response_data = self.make_request("https://www.ratemyprofessors.com/graphql", headers, payload)

                if "errors" in response_data:
                    print("GraphQL Errors:", response_data["errors"])

                teachers = response_data.get("data", {}).get("newSearch", {}).get("teachers", {}).get("edges", [])
                processed_teachers = self.process_teachers(teachers)
                all_results.extend(processed_teachers)

                print(f"Received {len(teachers)} teachers. Total results: {len(all_results)}")
                pageInfo = response_data.get("data", {}).get("newSearch", {}).get("teachers", {}).get("pageInfo", {})
                has_next_page = pageInfo.get("hasNextPage", False)
                cursor = pageInfo.get("endCursor", "")

            self.save_to_json(all_results)


if __name__ == "__main__":
    scraper = RateMyProfessorsScraper(school_id="U2Nob29sLTExMDA=")  # UF
    scraper.scrape_data()
    data = scraper.load_or_create_json()
    # course_reviews = scraper.get_course_reviews(data, "COT3100")
    # print(course_reviews)

