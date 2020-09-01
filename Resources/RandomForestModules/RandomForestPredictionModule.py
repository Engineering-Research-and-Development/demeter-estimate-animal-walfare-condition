import pandas as pd
import numpy as np
import joblib
import sys
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from util.logger import log
import json

class RandomForest:
    def execRFPrediction(self, JsonData):
        # LOGGING SETTINGS
        functionName = sys._getframe().f_code.co_name
        myLog = log()
        
        # LOADING MODELS SETTINGS
        modelsNotExists = False
        ModelFolderPath = './SavedModels'
        PrefixModel = 'Cow'
        LamenessModelName = PrefixModel + '_LamenessModel'
        KetosisModelName = PrefixModel + '_KetosisModel'
        MastitisModelName = PrefixModel + '_MastitisModel'
        
        myLog.writeMessage('Preparing to execute Random Forest Predictions of Estimate Animal Welfare Condition ...',3,functionName)
        # Estimate Animal Welfare Condition - Prediction
        with myLog.error_debug():
            try:

                # Check if models file exists
                myLog.writeMessage('Checking saved models files ...',3,functionName)
                if (os.path.exists(ModelFolderPath + '/' + LamenessModelName + '.pkl') and
                    os.path.exists(ModelFolderPath + '/' + KetosisModelName + '.pkl') and
                    os.path.exists(ModelFolderPath + '/' + MastitisModelName + '.pkl')):
                    myLog.writeMessage('Models files found!',1,functionName)
                    pass
                else :
                    # Models not exists
                    myLog.writeMessage('Models files not found!',2,functionName)
                    myLog.writeMessage('Listing existing fiels ...',1,functionName)
                    dup = []
                    filesNames = []
                    modelsNotExists = True
                    existingfiles = [f for f in os.listdir(ModelFolderPath) if os.path.isfile(os.path.join(ModelFolderPath, f))]
                    for i in existingfiles :
                        modelPrefix = i.split('_')[:-1]
                        if not(modelPrefix in dup):
                            filesNames.append(modelPrefix)
                            dup.append(modelPrefix)
                            print(dup,filesNames)
                    myLog.writeMessage('Listing existing files completed!',1,functionName)

                if not(modelsNotExists):
                    # Dataset preparation
                    myLog.writeMessage('Loading dataset ...',3,functionName)
                    JsonObj = json.loads(JsonData)
                    dataframe = pd.DataFrame(JsonObj)
                    dataframe = dataframe.set_index('Index')

                    LamenessCols = ['Total Daily Lying']
                    KetosisCols = ['Daily Fat', 'Daily Proteins', 'Daily Fat/Proteins']
                    MastitisCols = ['Conduttivity 1', 'Conduttivity 2', 'Conduttivity 3']

                    LamenessDS = dataframe[LamenessCols]
                    KetosisDS = dataframe[KetosisCols]
                    MastitisDS = dataframe[MastitisCols]
                    myLog.writeMessage('Dataset successfully loaded!',1,functionName)

                    # Loading random forest saved models
                    myLog.writeMessage('Loading models ...',3,functionName)
                    LamenessClassifier = joblib.load(ModelFolderPath + '/' + LamenessModelName + '.pkl')
                    KetosisClassifier = joblib.load(ModelFolderPath + '/' + KetosisModelName + '.pkl')
                    MastitisClassifier = joblib.load(ModelFolderPath + '/' + MastitisModelName + '.pkl')
                    myLog.writeMessage('Models successfully loaded!',1,functionName)

                    # Execute predictions
                    myLog.writeMessage('Executing predictions ...',3,functionName)
                    LamenessPred = LamenessClassifier.predict(LamenessDS)
                    KetosisPred = KetosisClassifier.predict(KetosisDS)
                    MastitisPred = MastitisClassifier.predict(MastitisDS)
                    myLog.writeMessage('Predictions successfully completed!',1,functionName)

                    # Predictions output preparation
                    myLog.writeMessage('Output preparation ...',3,functionName)
                    le = LabelEncoder()
                    le.fit(['Healthy','Sick']) # Healthy = 0 , Sick = 1
                    dataframe['PredictedLameness'] = le.inverse_transform(LamenessPred)
                    dataframe['PredictedKetosis'] = le.inverse_transform(KetosisPred)
                    dataframe['PredictedMastitis'] = le.inverse_transform(MastitisPred)
                    dataframe = dataframe.reset_index()
                    myLog.writeMessage('Output preparation completed!',1,functionName)
                    
                    # Json Output
                    #  TO DO... 
                    myLog.writeMessage('JSON output successfully processed!',1,functionName)
                    myLog.writeMessage('Estimate Animal Welfare Condition training and test completed!',1,functionName)
                    myLog.writeMessage('==============================================================',4,functionName)

                    ResultPred = dataframe
                else :
                    if len(existingfiles) < 1 :
                        myLog.writeMessage('The folder is empty!',2,functionName)
                        ResultPred = pd.DataFrame(0,index=range(1),columns=range(1))
                    else :
                        myLog.writeMessage('Model name not found!',2,functionName)
                        myLog.writeMessage('Found '+str(len(existingfiles))+' models files:'+ str(filesNames),2,functionName)
                        ResultPred = pd.DataFrame(0,index=range(1),columns=range(1))          
            except:
                myLog.writeMessage('Warning an exception occured!', 2,functionName)
                raise
print(ResultPred)