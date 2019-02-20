import webapp2
import template_engine
import logging
from gpuModel import GpuModel
from google.appengine.ext import ndb
from library.validation import Validation
import datetime


class GpuPage(webapp2.RequestHandler):
    template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/index.html')
    errors = []

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = self.request.path
        params = self.request.params
        if len(params) > 0 and 'gpu_name' not in params:
            # logging.info(self.request.params['gpu_name'])
            self.redirect('/gpu')
            return
        if path == "/gpu":
            self.index()
        elif path == "/gpu/new":
            self.new_gpu_get()
        elif "/gpu/edit" in path:
            self.edit_gpu_get()
        elif "/gpu/view" in path:
            self.get_view()
        elif path == "/gpu/search":
            self.get_search()
        elif path == "/gpu/compare":
            self.get_compare()
        elif path == "/gpu/selection":
            self.get_compare()
        logging.info(self.request.path)

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        formName = self.request.get('form')
        if formName == "new_gpu" or formName == "edit_gpu":
            self.new_gpu_post(formName)
        elif formName == "search_feature":
            self.post_search()


    def index(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/index.html')
        query = GpuModel.query()
        gpus = query.fetch()
        logging.info(query.fetch(projection=[GpuModel.name]))
        for val in query.fetch(projection=[GpuModel.name]):
            logging.info(val.name)
        data = {
            "gpus": gpus
        }
        self.response.write(template.render(data))

    def new_gpu_get(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/new.html')
        self.response.write(template.render({}))

    def edit_gpu_get(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/edit.html')
        query = GpuModel.query(GpuModel.name == self.request.params['gpu_name'])
        gpu = query.fetch()
        logging.info(gpu)
        if len(gpu) == 0:
            self.redirect('/gpu')
            return
        data = {
            "gpu": gpu[0]
        }
        logging.info(gpu[0].name)
        self.response.write(template.render(data))

    def new_gpu_post(self, form_name):
        GpuPage.errors = []

        geometryShader = False
        if self.request.get('geometryShader'):
            geometryShader = True

        tesselationShader = False
        if self.request.get('tesselationShader'):
            tesselationShader = True

        shaderInt16 = False
        if self.request.get('shaderInt16'):
            shaderInt16 = True

        sparseBinding = False
        if self.request.get('sparseBinding'):
            sparseBinding = True

        textureCompressionETC2 = False
        if self.request.get('textureCompressionETC2'):
            textureCompressionETC2 = True

        vertexPipelineStoresAndAtomics = False
        if self.request.get('vertexPipelineStoresAndAtomics'):
            vertexPipelineStoresAndAtomics = True

        name = self.request.get('name')
        if form_name != "edit_gpu" and Validation.is_empty(name):
            GpuPage.errors.append('GPU name can not be empty')

        if form_name == "edit_gpu":
            name = self.request.params['gpu_name']

        manufacturer = self.request.get('manufacturer')
        if Validation.is_empty(manufacturer):
            GpuPage.errors.append('Manufacturer name can not be empty')

        date = self.request.get('date')
        if Validation.is_empty(date):
            GpuPage.errors.append('Manufactured date can not be empty')
        if form_name == "edit_gpu":
            GpuModel_key = ndb.Key('GpuModel', name)
            Gpu = GpuModel_key.get()
            if Gpu == None:
                self.redirect("/gpu")
        if len(GpuPage.errors) == 0:
            GpuModel_key = ndb.Key('GpuModel', name)
            Gpu = GpuModel_key.get()
            if form_name == "new_gpu" and Gpu != None:
                GpuPage.errors.append("thia gpu already exist")
            else:
                newGpu = GpuModel(id=name, name=name, manufacturer=manufacturer,
                                  date=datetime.datetime.strptime(date, '%Y-%m-%d'), geometryShader=geometryShader,
                                  tesselationShader=tesselationShader,
                                  shaderInt16=shaderInt16, sparseBinding=sparseBinding,
                                  textureCompressionETC2=textureCompressionETC2,
                                  vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)

                newGpu.put()

        if form_name == "new_gpu":
            template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/new.html')
            data = {
                "errors": GpuPage.errors
            }
        else:
            query = GpuModel.query(GpuModel.name == self.request.params['gpu_name'])
            gpu = query.fetch()
            data = {
                "gpu": gpu[0],
                "errors": GpuPage.errors
            }
            template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/edit.html')
        self.response.write(template.render(data))

    def get_view(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/view.html')
        query = GpuModel.query(GpuModel.name == self.request.params['gpu_name'])
        gpu = query.fetch()
        logging.info(gpu)
        if len(gpu) == 0:
            self.redirect('/gpu')
            return
        data = {
            "gpu": gpu[0]
        }
        logging.info(gpu[0].name)
        self.response.write(template.render(data))

    def get_search(self):
        pass

    def get_gpu_selection(self):
        pass

    def get_compare(self):
        pass

    def post_search(self):
        pass


app = webapp2.WSGIApplication([
    ('/gpu', GpuPage),
    ('/gpu/new', GpuPage),
    ('/gpu/edit', GpuPage),
    ('/gpu/view', GpuPage),
    ('/gpu/search', GpuPage),
    ('/gpu/compare', GpuPage),
    ('/gpu/selection', GpuPage)
], debug=True)
