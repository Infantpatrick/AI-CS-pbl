import unittest
from unittest.mock import patch, MagicMock
import torch

from src.model.prediction_pipeline import PhishingPredictor

class TestThresholdBoundary(unittest.TestCase):
    @patch('src.model.prediction_pipeline.BertForSequenceClassification.from_pretrained')
    @patch('src.model.prediction_pipeline.BertTokenizerFast.from_pretrained')
    def test_threshold_boundaries(self, mock_tokenizer_init, mock_model_init):
        # Setup mock model
        mock_model = MagicMock()
        mock_model_init.return_value = mock_model
        
        # Setup mock tokenizer
        mock_tokenizer = MagicMock()
        mock_tokenizer.return_value = {
            'input_ids': torch.tensor([[1, 2, 3]]),
            'attention_mask': torch.tensor([[1, 1, 1]])
        }
        mock_tokenizer_init.return_value = mock_tokenizer
        
        predictor = PhishingPredictor()

        # Test < 0.70 -> Legitimate
        with patch('src.model.prediction_pipeline.F.softmax') as mock_softmax:
            mock_softmax.return_value = torch.tensor([[0.301, 0.699]])
            result = predictor.predict_email("Subj", "Body")
            self.assertEqual(result["prediction"], "Legitimate")
            self.assertEqual(result["phishing_probability"], 0.699)

        # Test == 0.70 -> Legitimate
        with patch('src.model.prediction_pipeline.F.softmax') as mock_softmax:
            mock_softmax.return_value = torch.tensor([[0.300, 0.700]])
            result = predictor.predict_email("Subj", "Body")
            self.assertEqual(result["prediction"], "Legitimate")
            self.assertEqual(result["phishing_probability"], 0.700)

        # Test > 0.70 -> Phishing
        with patch('src.model.prediction_pipeline.F.softmax') as mock_softmax:
            mock_softmax.return_value = torch.tensor([[0.299, 0.701]])
            result = predictor.predict_email("Subj", "Body")
            self.assertEqual(result["prediction"], "Phishing")
            self.assertEqual(result["phishing_probability"], 0.701)

if __name__ == '__main__':
    unittest.main()
