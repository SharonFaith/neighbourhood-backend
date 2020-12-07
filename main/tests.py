from django.test import TestCase
from .models import Hood, Post, Category, Comment, Service
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class TestHood(TestCase):
    """
    """
    def setUp(self):
        self.hood = Hood.objects.create(name='Hood 1', local_area="Kilimani", city_town='Nr', country='Mm')
        #self.user = User.objects.create(first_name='John', last_name='Doe', email='johndoe@example.com', username='john_doe', password='password')

    def tearDown(self):
        Hood.objects.all().delete()

    def test_instance(self):
        """
        Test if instance of Hood
        """
        self.assertIsInstance(self.hood, Hood)

    def test_attributes(self):
        """
        Test if attributes are createed correctly
        """
        self.assertEqual(self.hood.name, 'Hood 1')
        self.assertEqual(self.hood.local_area, 'Kilimani')
        self.assertEqual(self.hood.city_town, 'Nr')
        self.assertEqual(self.hood.country, 'Mm')
       
    
    def test_save_hood(self):

        self.hood.save_hood()
        hoods = Hood.objects.all()

        self.assertTrue(len(hoods) > 0)

    def test_delete_hood(self):
        self.hood.save_hood()
        new2 = Hood(name='hood2', local_area='mil', city_town='eld', country='xyz')
        new2.save_hood()

        new2.delete_hood()
        
        hoods = Hood.objects.all()

        self.assertTrue(len(hoods) == 1)

    def test_update_hood(self):
        self.hood.save_hood()
        #print(self.new.id)
        new2 = Hood(name='hood2', local_area='mil', city_town='eld', country='xyz')
        new2.save_hood()
        print("update hood")
        print(new2.id)

        Hood.update_hood(15,'the new place')
       
        self.assertEqual(Hood.objects.filter(id = 15).first().name, 'the new place')

    
    def test_get_hood_by_id(self):

        self.hood.save_hood()
        
        new2 = Hood(name='hood2', local_area='mil', city_town='eld', country='xyz')
        new2.save_hood()
        #print(new2.id)

        Hood.get_hood_by_id(11)

        self.assertEqual(Hood.objects.filter(id = 11).first().name, 'hood2')


class TestPost(TestCase):
    """
    Test post model   
    """
    def setUp(self):

        self.hood = Hood.objects.create(name='Hood 1', local_area="Kilimani", city_town='Nr', country='Mm')
        self.user = User.objects.create(first_name='John', last_name='Doe', email='johndoe@example.com', username='john_doe', password='password')


        self.post = Post.objects.create(hood= self.hood, user= self.user, content='post')
        
    def tearDown(self):
        Post.objects.all().delete()

    def test_instance(self):
        """
        Test if instance of Post
        """
        self.assertIsInstance(self.post, Post)

    def test_attributes(self):
        """
        Test if attributes are createed correctly
        """
        self.assertEqual(self.post.hood, self.hood)
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.content, 'post')
       
       
    
    def test_save_post(self):

        self.post.save_post()
        posts = Post.objects.all()

        self.assertTrue(len(posts) > 0)

    def test_delete_post(self):
        self.post.save_post()
        new2 = Post(hood= self.hood, user= self.user, content='another post')
        new2.save_post()

        new2.delete_post()
       
        posts = Post.objects.all()

        self.assertTrue(len(posts) == 1)

    def test_update_post(self):
        self.post.save_post()
        #print(self.new.id)
        new2 = Post(hood= self.hood, user= self.user, content='another post')
        new2.save_post()
        #print('post id')
        print(new2.id)

        Post.update_post(15,'the new place')
       
        self.assertEqual(Post.objects.filter(id = 15).first().content, 'the new place')

    
    def test_get_post_by_id(self):

        self.post.save_post()
        
        new2 = Post(hood= self.hood, user= self.user, content='another post')
        new2.save_post()
        #print('the_post id')
        #print(new2.id)

        Post.get_post_by_id(11)

        self.assertEqual(Post.objects.filter(id = 11).first().content, 'another post')

class TestCategory(TestCase):
    """
    Test category model   
    """
    def setUp(self):

        self.category = Category(name='cream')
        
    def tearDown(self):
        Category.objects.all().delete()

    def test_instance(self):
        """
        Test if instance of Category
        """
        self.assertIsInstance(self.category, Category)

    def test_attributes(self):
        """
        Test if attributes are created correctly
        """
        self.assertEqual(self.category.name, 'cream')
    
    
    def test_save_category(self):

        self.category.save_category()
        categories = Category.objects.all()

        self.assertTrue(len(categories) > 0)

    def test_delete_category(self):
        self.category.save_category()
        new2 = Category(name='dairy')
        new2.save_category()

        new2.delete_category()
       
        categories = Category.objects.all()

        self.assertTrue(len(categories) == 1)

    def test_update_category(self):
        self.category.save_category()
        #print(self.new.id)
        new2 = Category(name='dairy')
        new2.save_category()
        print(new2.id)

        Category.update_category(7,'other')
       
        self.assertEqual(Category.objects.filter(id = 7).first().name, 'other')

    
    def test_get_categ_by_id(self):

        self.category.save_category()
        
        new2 = Category(name='dairy')
        new2.save_category()
        print(new2.id)

        Category.get_categ_by_id(4)

        self.assertEqual(Category.objects.filter(id = 4).first().name, 'dairy')

class TestService(TestCase):
    """
    Test service model   
    """
    def setUp(self):

        self.hood = Hood.objects.create(name='Hood 1', local_area="Kilimani", city_town='Nr', country='Mm')
        self.user = User.objects.create(first_name='John', last_name='Doe', email='johndoe@example.com', username='john_doe', password='password')
        self.category = Category.objects.create(name='categ')

        self.service = Service.objects.create(name='service', hood= self.hood, email='xyz@email.com', user = self.user, category = self.category, description='xyz')
        
    def tearDown(self):
        Service.objects.all().delete()

    def test_instance(self):
        """
        Test if instance of Service
        """
        self.assertIsInstance(self.service, Service)

    def test_attributes(self):
        """
        Test if attributes are createed correctly
        """
        self.assertEqual(self.service.hood, self.hood)
        self.assertEqual(self.service.user, self.user)
        self.assertEqual(self.service.category, self.category)
        self.assertEqual(self.service.email, 'xyz@email.com')
        self.assertEqual(self.service.name, 'service')
        self.assertEqual(self.service.description, 'xyz')
       
       
    
    def test_save_service(self):

        self.service.save_service()
        services = Service.objects.all()

        self.assertTrue(len(services) > 0)

    def test_delete_service(self):
        self.service.save_service()
        new2 = Service(name='service2', hood= self.hood, email='xyzz@email.com', user = self.user, category = self.category, description='describe xyz')
        new2.save_service()

        new2.delete_service()
       
        services = Service.objects.all()

        self.assertTrue(len(services) == 1)

    def test_update_service(self):
        self.service.save_service()
        #print(self.new.id)
        new2 = Service(name='service2', hood= self.hood, email='xyzz@email.com', user = self.user, category = self.category, description='describe xyz')
        new2.save_service()
        print(new2.id)

        Service.update_service(9,'newname')
       
        self.assertEqual(Service.objects.filter(id = 9).first().name, 'newname')

    
    def test_get_service_by_id(self):

        self.service.save_service()
        
        new2 = Service(name='service2', hood= self.hood, email='xyzz@email.com', user = self.user, category = self.category, description='describe xyz')
        new2.save_service()
        print(new2.id)

        Service.get_service_by_id(5)

        self.assertEqual(Service.objects.filter(id = 5).first().name, 'service2')

class TestComment(TestCase):
    """
    Test post model   
    """
    def setUp(self):
        self.hood = Hood.objects.create(name='Hood 1', local_area="Kilimani", city_town='Nr', country='Mm')
        self.user = User.objects.create(first_name='John', last_name='Doe', email='johndoe@example.com', username='john_doe', password='password')

        self.post = Post.objects.create(hood= self.hood, user= self.user, content='post')
        

        self.comment = Comment.objects.create(post= self.post, user= self.user, content='comment')
        
    def tearDown(self):
        Comment.objects.all().delete()

    def test_instance(self):
        """
        Test if instance of comment
        """
        self.assertIsInstance(self.comment, Comment)

    def test_attributes(self):
        """
        Test if attributes are createed correctly
        """
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, 'comment')
       
       
    
    def test_save_comment(self):

        self.comment.save_comment()
        comments = Comment.objects.all()

        self.assertTrue(len(comments) > 0)

    def test_delete_comment(self):
        self.comment.save_comment()
        new2 = Comment(post= self.post, user= self.user, content='another comment')
        new2.save_comment()

        new2.delete_comment()
       
        comments = Comment.objects.all()

        self.assertTrue(len(comments) == 1)

    def test_update_comment(self):
        self.comment.save_comment()
        new2 = Comment(post= self.post, user= self.user, content='another comment')
        new2.save_comment()
        print("comment_id:")
        print(new2.id)

        Comment.update_comment(9,'the new place')
       
        self.assertEqual(Comment.objects.filter(id = 9).first().content, 'the new place')

    
    def test_get_comment_by_id(self):

        self.comment.save_comment()
        
        self.comment.save_comment()
        new2 = Comment(post= self.post, user= self.user, content='another comment')
        new2.save_comment()
        
        print(new2.id)

        Comment.get_comment_by_id(5)

        self.assertEqual(Comment.objects.filter(id = 5).first().content, 'another comment')

