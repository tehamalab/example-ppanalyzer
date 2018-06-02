# -*- coding: utf-8 -*-

import os
import csv
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
import aiohttp.web


TRAIN_DATA = os.environ.get('PPANALYZER_TRAIN_DATA', '')


class Classifier:

    def __init__(self, train_data=None):

        self._classifier = None
        self.train_data = train_data

    def get_training_data(self):
        data = {'x': [], 'y': []}

        with open(self.train_data) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data['x'].append(row.get('text'))
                data['y'].append(row.get('class'))

        return data

    def train(self):

        self._classifier = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', SGDClassifier(loss='log', penalty='l2',
                                  alpha=1e-3, tol=None,
                                  random_state=42,
                                  max_iter=5))
        ])

        data = self.get_training_data()
        self._classifier.fit(data['x'], data['y'])

    def predict(self, text):
        if isinstance(text, str):
            text = [text]
        return self._classifier.predict(text)


routes = aiohttp.web.RouteTableDef()


@routes.get('/')
async def home(request):
    return aiohttp.web.FileResponse(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'public/index.html'
        )
    )


@routes.get('/analyze')
async def analyze_handler(request):
    text = request.query.get('text')

    if not text:
        return aiohttp.web.json_response({'class': None})

    return aiohttp.web.json_response(
        {'class': request.app['classifier'].predict(text)[0]}
    )


def get_app(**kwargs):
    app = aiohttp.web.Application(**kwargs)
    app.add_routes(routes)

    app['classifier'] = Classifier()
    app['classifier'].train_data = TRAIN_DATA
    app['classifier'].train()
    return app


def web(**kwargs):
    app = get_app()
    aiohttp.web.run_app(app, **kwargs)
