from flask import Flask, render_template
from post import Post
import requests

# Fetching posts from the API
response = requests.get("https://api.npoint.io/5abcca6f4e39b4955965")

# Checking if the request was successful (status code 200)
if response.status_code == 200:
    posts = response.json()
else:
    # If the request was not successful, print an error message and exit
    print(f"Error fetching posts. Status code: {response.status_code}")
    exit()

post_objects = []

# Checking if the received data is a list
if isinstance(posts, list):
    for post in posts:
        # Checking if the necessary keys exist in each post
        if all(key in post for key in ["id", "title", "subtitle", "body"]):
            post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
            post_objects.append(post_obj)
        else:
            print("Invalid post format. Skipping.")
else:
    print("Invalid data format. Expected a list of posts.")

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = next((blog_post for blog_post in post_objects if blog_post.id == index), None)

    if requested_post:
        return render_template("post.html", post=requested_post)
    else:
        return "Post not found", 404


if __name__ == "__main__":
    app.run(debug=True)
