import keras


class SalaryPredictor:
    def __init__(self):
        keras.backend.clear_session()
        self.model = self.nn()
        self.model_json_path = "storage/salary_predictor.json"
        self.model_h5_path = "storage/salary_predictor.h5"
        # self.model = self.load()

    @staticmethod
    def nn():
        feat_vec = keras.layers.Input(shape=(128,))

        x = keras.layers.Dense(64, activation="relu")(feat_vec)
        x = keras.layers.Dropout(0.3)(x)

        x = keras.layers.Dense(64, activation="relu")(feat_vec)
        x = keras.layers.Dropout(0.3)(x)

        x = keras.layers.Dense(64, activation="relu")(feat_vec)
        x = keras.layers.Dropout(0.3)(x)

        out = keras.layers.Dense(2)(x)

        model = keras.models.Model(inputs=feat_vec, outputs=out)
        model.compile(
            loss="mean_squared_error", optimizer=keras.optimizers.Adam(lr=1e-3)
        )

        return model

    def save(self):
        with open(self.model_json_path, "w") as f:
            f.write(model.to_json())
        model.save_weights(self.model_h5_path)
        print("model saved")

    def load(self):
        json_file = open(self.model_json_path, "r")
        model = json_file.read()
        json_file.close()
        model = model_from_json(model)
        # load weights into new model
        model.load_weights(self.model_h5_path)
        self.model = model
        self.model._make_predict_function()

    def predict(self, feat_vec):
        return self.model.predict(feat_vec)[0][0]


# export
salary_predictor = SalaryPredictor()
