import webapp2
import template_engine
import logging
from models.gpuModel import GpuModel
from google.appengine.ext import ndb
from library.validation import Validation
import datetime
from library.user import User

class GpuPage(webapp2.RequestHandler):
    template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/index.html')
    errors = []

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = self.request.path

        if path == "/gpu" or path == "/":
            self.index()
        elif path == "/gpu/new":
            self.new_gpu_get()
        elif "/gpu/edit" in path:
            self.edit_gpu_get()
        elif "/gpu/view" in path:
            self.get_view()
        elif path == "/gpu/search":
            self.get_search()
        elif "/gpu/compare" in path:
            self.get_compare()
        elif path == "/gpu/selection":
            self.gpu_selection()
        logging.info(self.request.path)

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        formName = self.request.get('form')
        logging.info(formName)
        if formName == "new_gpu" or formName == "edit_gpu":
            self.new_gpu_post(formName)
        elif formName == "search_feature":
            self.post_search()
        elif formName == "compare_gpu":
            self.gpu_selection()

    def index(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/index.html')
        query = GpuModel.query()
        gpus = query.fetch()
        logging.info(query.fetch(projection=[GpuModel.name]))
        for val in query.fetch(projection=[GpuModel.name]):
            logging.info(val.name)

        user = User.get_user(self)
        data = {
            "gpus": gpus,
            'url': user["url"],
            'url_string': user['url_string'],
        }
        self.response.write(template.render(data))

    def new_gpu_get(self):
        params = self.request.params
        if len(params) > 0 and 'gpu_name' not in params:
            # logging.info(self.request.params['gpu_name'])
            self.redirect('/')
            return
        user = User.get_user(self)
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/new.html')
        self.response.write(template.render({'url': user["url"],'url_string': user['url_string']}))

    def edit_gpu_get(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/edit.html')
        query = GpuModel.query(GpuModel.name == self.request.params['gpu_name'])
        gpu = query.fetch()
        logging.info(gpu)
        if len(gpu) == 0:
            self.redirect('/')
            return
        user = User.get_user(self)
        data = {
            "gpu": gpu[0],
            'url': user["url"],
            'url_string': user['url_string'],
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
                self.redirect("/")
        if len(GpuPage.errors) == 0:
            GpuModel_key = ndb.Key('GpuModel', name)
            Gpu = GpuModel_key.get()
            if form_name == "new_gpu" and Gpu != None:
                GpuPage.errors.append("This GPU already exists")
            else:
                newGpu = GpuModel(id=name, name=name, manufacturer=manufacturer,
                                  date=datetime.datetime.strptime(date, '%Y-%m-%d'), geometryShader=geometryShader,
                                  tesselationShader=tesselationShader,
                                  shaderInt16=shaderInt16, sparseBinding=sparseBinding,
                                  textureCompressionETC2=textureCompressionETC2,
                                  vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)

                newGpu.put()
        user = User.get_user(self)
        message = ""
        if form_name == "new_gpu":
            template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/new.html')
            if not GpuPage.errors:
                message = "GPU saved successfully"
            data = {
                "errors": GpuPage.errors,
                'url': user["url"],
                'url_string': user['url_string'],
                'message': message
            }
        else:
            query = GpuModel.query(GpuModel.name == self.request.params['gpu_name'])
            gpu = query.fetch()
            if not GpuPage.errors:
                message = "GPU updated successfully"
            data = {
                "gpu": gpu[0],
                "errors": GpuPage.errors,
                'url': user["url"],
                'url_string': user['url_string'],
                'message': message
            }
            template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/edit.html')

        self.response.write(template.render(data))

    def get_view(self):
        params = self.request.params
        if len(params) > 0 and 'gpu_name' not in params:
            # logging.info(self.request.params['gpu_name'])
            self.redirect('/')
            return
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/view.html')
        query = GpuModel.query(GpuModel.name == self.request.params['gpu_name'])
        gpu = query.fetch()
        logging.info(gpu)
        if len(gpu) == 0:
            self.redirect('/')
            return
        user = User.get_user(self)
        data = {
            "gpu": gpu[0],
            'url': user["url"],
            'url_string': user['url_string'],
        }
        logging.info(gpu[0].name)
        self.response.write(template.render(data))

    def get_search(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/search.html')
        user = User.get_user(self)
        self.response.write(template.render({'url': user["url"],'url_string': user['url_string']}))

    def gpu_selection(self):
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/gpu_selection.html')
        query = GpuModel.query(projection=[GpuModel.name])
        logging.info(query)
        form = self.request.get('form')
        gpu1 = self.request.get('gpu1')
        gpu2 = self.request.get('gpu2')
        error = []
        if form:
            if gpu1 == gpu2:
                error.append("Please select two type of GPUs to compare")
            else:
                self.redirect('/gpu/compare?' + "gpu1=" + gpu1 + "&" + "gpu2=" + gpu2)
                return
        user = User.get_user(self)
        data = {
            "gpus": query,
            "errors": error,
            'url': user["url"],
            'url_string': user['url_string'],
        }
        self.response.write(template.render(data))

    def get_compare(self):
        params = self.request.params
        if len(params) > 0 and 'gpu1' not in params or 'gpu2' not in params:
            # logging.info(self.request.params['gpu_name'])
            self.redirect('/')
            return
        gpu1_key = ndb.Key('GpuModel', params['gpu1'])
        Gpu1 = gpu1_key.get()

        gpu2_key = ndb.Key('GpuModel', params['gpu2'])
        Gpu2 = gpu2_key.get()

        if not Gpu1 or not Gpu2:
            self.redirect("/")
            return
        user = User.get_user(self)
        data = {
            "gpu1": Gpu1,
            "gpu2": Gpu2,
            'url': user["url"],
            'url_string': user['url_string'],
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/compare.html')
        self.response.write(template.render(data))

    def post_search(self):
        params = []
        error = ""
        if self.request.get('geometryShader'):
            params.append(GpuModel.geometryShader == True)

        if self.request.get('tesselationShader'):
            params.append(GpuModel.tesselationShader == True)

        if self.request.get('shaderInt16'):
            params.append(GpuModel.shaderInt16 == True)

        if self.request.get('sparseBinding'):
            params.append(GpuModel.sparseBinding == True)

        if self.request.get('textureCompressionETC2'):
            params.append(GpuModel.textureCompressionETC2 == True)

        if self.request.get('vertexPipelineStoresAndAtomics'):
            params.append(GpuModel.vertexPipelineStoresAndAtomics == True)

        result = []
        if len(params) == 0:
            error = "Please select an option"
        else:
            query = GpuModel.query(*params)
            result = query.fetch()
            if len(result) == 0:
                error = "There is no GPU available with this selection"
        user = User.get_user(self)
        template = template_engine.JINJA_ENVIRONMENT.get_template('layouts/gpu/search.html')
        self.response.write(template.render({"results":result,"errors":error,'url': user["url"],'url_string': user['url_string']}))


app = webapp2.WSGIApplication([
    ('/', GpuPage),
    ('/gpu/new', GpuPage),
    ('/gpu/edit', GpuPage),
    ('/gpu/view', GpuPage),
    ('/gpu/search', GpuPage),
    ('/gpu/compare', GpuPage),
    ('/gpu/selection', GpuPage)
], debug=True)
