import requests, json, os
class GideonAPI:
    https = "https://api.gideononline.com/"
    def __init__(self):
        self.headers = {"Authorization": f"api_key {os.environ.get('GIDEON_API_KEY')}"}
    def set_path(self, path):
        self.path = path
    def make_endpoint(self, action, query = ""):
        endpoint = self.https + action + query
        print(endpoint)
        return endpoint
    def get_request(self, action, query = ""):
        url = self.make_endpoint(action, query)
        return requests.get(url,headers = self.headers).json()
    def get_disease_by_filter(self, filter = None):
        #?filter=VAL
        if filter:
            return self.get_request("diseases/filter", query = f"?{filter}")
        else:
            return self.get_request("diseases")
    def set_disease_codes(self, dict):
        self.disease_codes = []
        for filter_key in [*dict]:
             for disease in (dict.get(filter_key)):
                print(disease)
                self.disease_codes.append(disease["disease_code"])
    def get_disease_identifiers(self,filter_key = "vector"):
        self.disease_disease_code_dic = {}
        for vector in vector_list["data"]:
            if (vector[f"{filter_key}_code"] != None) and (vector[f"{filter_key}_code"] != "N"):
                filter_code = vector[f"{filter_key}_code"]
                disease_by_key_dic = gideon_api.get_disease_by_filter(f"{filter_key}={filter_code}")
                disease_by_key_dic[filter_code] = disease_by_key_dic.pop("data")
                self.disease_disease_code_dic.update(disease_by_key_dic)
    def get_data_by_disease_code(self):
        self.disease_data_dic = {}
        for disease_code in self.disease_codes:
            disease_data = (gideon_api.get_request(f"/diseases/{disease_code}/general"))
            self.disease_data_dic[disease_code] = disease_data["data"]
            print(self.disease_data_dic)
        return self.disease_data_dic
    def save_file(self, data, filename, ext = ".json"):
        filename_ext = filename + ext
        fullpath = os.path.join(self.path, filename_ext)
        if ext == ".json":
            with open(fullpath, 'w+') as f:  
                json.dump(data, f)
                f.close        

gideon_api = GideonAPI()
gideon_api.set_path("INSERT PATH")
vector_list = gideon_api.get_request("diseases/fingerprint/vectors")
gideon_api.set_disease_codes(vector_list)
gideon_api.get_data_by_disease_code()
gideon_api.save_file(data=gideon_api.disease_data_dic,filename="vbd_data_vector",ext=".json")




