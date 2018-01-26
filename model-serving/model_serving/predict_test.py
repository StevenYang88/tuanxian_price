import sys
#
# print('Python %s on %s' % (sys.version, sys.platform))
#
# sys.path.extend(["C:/Users/Chinalife/Documents/机器学习/团险报价/团险定价归档/团险定价归档/model-serving/model_serving"])
print(sys.path)

from model_serving.proto.model_info_pb2 import insurance_price
from model_serving.service.insurance_price_service import InsurancePriceService
from model_serving.setting import Setting

# data = pd.read_csv('./data/pre_test.csv', header=None)
#
#
# def load_model(path):
#     """
#     加载模型
#     :return:
#     """
#     model = model_from_json(open('data/insurance_price/' + path + '/keras/keras_network.json').read())
#     model.load_weights('data/insurance_price/' + path + '/keras/keras_weights.h5')
#     return model
#
#
# def predict(data_set,model):
#     x = data_set.values
#     yp = model.predict(x).transpose()
#     print([x,yp])
#
#
# if __name__ == '__main__':
#     model1 = load_model('keras_avg_claim')
#     model2 = load_model('keras_avg_days')
#     model3 = load_model('keras_avg_pay')
#     model4 = load_model('keras_risk_ratio')
#     predict(data, model1)
#     predict(data, model2)
#     predict(data, model3)
#     predict(data, model4)
if __name__ == '__main__':

    conf = "conf/model-serving.json"
    data = '{"request_id":"req_id","policy":"889","coverage":6,"industry":13,"occupation":24,"city":"440800","amount":1000000.00,"num":20,"avg_age":40,"sex_ratio":0.6}'

    setting = Setting(conf)
    insurance_price_service = \
        InsurancePriceService(setting.get_model_info(insurance_price))

    response = insurance_price_service.inference(data)
    print(response)

