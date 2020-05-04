import torch
from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2, output_attentions=False, output_hidden_states=False)
model.load_state_dict(torch.load('model.pt', map_location='cpu'))
model.eval()


def score_tweet(text, tokenizer, model):

	# Encode the text
	encoded_dict = tokenizer.encode_plus(text, add_special_tokens = True, max_length=160, pad_to_max_length=True, return_tensors='pt', return_attention_mask=True) 

	# Set the device to CPU
	device = torch.device('cpu')
	input_ids = torch.tensor(encoded_dict['input_ids']).to(device)
	attention_masks = torch.tensor(encoded_dict['attention_mask']).to(device)

	# Get our raw outputs
	outputs = model(input_ids, token_type_ids=None, attention_mask=attention_masks)[0]

	# Get the probability of positive sentiment
	sm = torch.nn.Softmax()
	probabilities = sm(outputs) 
	pos_prob = torch.Tensor.cpu(probabilities).detach().numpy()[:,0][0]
	return pos_prob


score_tweet("Hello frriend", tokenizer, model)