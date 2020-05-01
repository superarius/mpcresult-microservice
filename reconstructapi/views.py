from django.shortcuts import render
from django.http import JsonResponse
import requests
from reconstructapi.serialize import deserialize_shares
from reconstructapi.shamir import Shamir

def home(request):
	cid = request.GET.get("computation_id", None)
	r = requests.get("https://safetraceapi.herokuapp.com/api/results", json={'computation_id':cid}, headers={"api_key": "4b6bff10-760e-11ea-bcd4-03a854e8623c"})
	j = json.loads(r.text)
	raw_shares = j["shares"]
	aid_shares = {}
	seen = []
	for r in raw_shares:
		if r["area_id"] not in seen:
			seen.append(r["area_id"])
			aid_shares[r["area_id"]] = []
		shares = deserialize_shares(json.loads(r["share"]))
		aid_shares[r["area_id"]].append(shares)
	output_dict = {}
	for aid, shares in aid_shares.items():
		le_score=Shamir(1, 3).reconstruct_bitstring_secret(shares)
		be_score = le_score[::-1]
		output_dict[aid] = int(be_score, 2)
	return JsonResponse(output_dict)

