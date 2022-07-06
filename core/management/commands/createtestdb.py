import random
import requests
import urllib
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand
from django.core.files import File

from core.models import User
from posts.models import Post

usernames = ["test", "user", "dummy"]
posts = ["description", "test", "dummy", "#tag", "#lol", "#mem"]

def get_random_cat_image():
    req = requests.get("http://aws.random.cat/meow")
    print(req.content)
    file_url = req.json().get("file")
    name = urllib.parse.urlparse(file_url).path.split('/')[-1]
    content = urllib.request.urlretrieve(file_url)
    return name, File(open(content[0], "rb"))


class Command(BaseCommand):
    help = "Init test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-pictures",
            default=False,
            help="Include pictures or not"
        )

    def handle(self, *args, **options):
        for i in range(random.randint(3, 7)):
            username = f"{random.choice(usernames)}{i}"
            user = User.objects.filter(username=username).first()
            if not user:
                user = User(
                    username=username,
                    email=f"{username}@email.com",
                    first_name=username.capitalize(),
                    last_name=username.capitalize(),
                )
                if options.get("with-pictures"):
                    user.avatar.save(*get_random_cat_image())
                user.set_password(username)
                user.save()
            self.stdout.write(f"Created user {user}")
            for _ in range(random.randint(5, 10)):
                description = " ".join(random.choices(posts, k=random.randint(3, 5)))
                post = Post(
                    description=description,
                    user=user, 
                )
                if options.get("with-pictures"):
                    post.image.save(*get_random_cat_image())
                post.save()
                self.stdout.write(f"Created post {post}")
        self.stdout.write("SUCCESS!")

