from flexml.regression import Regression
from parameterized import parameterized
import unittest
import pandas as pd

from flexml.logger.logger import get_logger

class TestRegression(unittest.TestCase):
    df = pd.read_csv("tests/test_data/wine_regression.csv")
    logger = get_logger(__name__)
    logger.setLevel("DEBUG")
    
    @parameterized.expand(["quick", "wide"])
    def test_regression(self, exp_size: str, df: pd.DataFrame = df):
        try:
            reg_exp = Regression(
                data = df,
                target_col = "Customer_Segment",
                experiment_size = exp_size,
                test_size = 0.25,
                random_state = 42,
                logging_to_file = True
            )
        except Exception as e:
            error_msg = f"An error occured while setting up {exp_size} regression, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        try:
            reg_exp.start_experiment(top_n_models = 1)
        except Exception as e:
            error_msg = f"An error occured while running {exp_size} regression experiment, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        top_x_models = reg_exp.get_best_models(top_n_models = 3)
        if len(top_x_models) != 3:
            error_msg = f"An error occured while retriving the best models in {exp_size} regression, expected 3, got {len(top_x_models)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
                
        try:
            reg_exp.show_model_stats()
        except Exception as e:
            error_msg = f"An error occured while showing models stats in {exp_size} regression, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        try:
            reg_exp.tune_model(n_trials=3, cv = 2)

            if reg_exp.tuned_model is None:
                error_msg = f"An error occured while tuning the model in {exp_size} regression, tuned model is None"
                self.logger.error(error_msg)
                raise Exception(error_msg)
                        
            if reg_exp.tuned_model_score is None:
                error_msg = f"An error occured while calculating the tuned model's score in {exp_size} regression, tuned model score is None"
                self.logger.error(error_msg)
                raise Exception(error_msg)
                    
        except Exception as e:
            error_msg = f"An error occured while tuning the model in {exp_size} regression, Error: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg)