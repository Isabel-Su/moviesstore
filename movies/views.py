from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = movie.review_set.filter(is_reported=False)
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method != 'POST':
        return redirect('movies.show', id=id)
    comment = request.POST.get('comment', '').strip()
    rating = request.POST.get('rating', '')

    if not comment or len(comment) > 255:
        return HttpResponseBadRequest('Enter a comment between 1 and 255 characters')

    if rating not in ('1','2','3','4','5'):
        return HttpResponseBadRequest('Choose a rating from 1 to 5.')

    movie = get_object_or_404(Movie, id=id)
    Review.objects.create(
        comment = comment,
        rating = int(rating),
        movie = movie,
        user = request.user,

    ) 
    return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        rating = request.POST.get('rating', '')

        if not comment or len(comment) > 255:
            return HttpResponseBadRequest('Enter a comment between 1 and 255 characters')
        if rating not in ('1','2','3','4','5'):
            return HttpResponseBadRequest('Choose a rating from 1 to 5.')
    
        review.comment = comment
        review.rating = int(rating)
        review.save()
        return redirect('movies.show', id=id)

    template_data = {'title': 'Edit Review',
                     'review': review,
                     'rating_choices': range(1,6),
                     }
    return render(request, 'movies/edit_review.html',
                  {'template_data': template_data})

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_reported = True
    review.save()
    return redirect('movies.show', id=id)
