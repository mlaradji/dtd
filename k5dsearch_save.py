version+=1

with open("K5dsearch_version.file", "wb") as f:
    pickle.dump(version, f, pickle.HIGHEST_PROTOCOL)
    
with open("K5dsearch_Gseq_"+str(version)+".file", "wb") as f:
    pickle.dump(Gseq, f, pickle.HIGHEST_PROTOCOL)
    
with open("K5dsearch_SVseq_"+str(version)+".file", "wb") as f:
    pickle.dump(SVseq, f, pickle.HIGHEST_PROTOCOL) 
    
with open("K5dsearch_expanded_"+str(version)+".file", "wb") as f:
    pickle.dump(expanded, f, pickle.HIGHEST_PROTOCOL)
    
with open("K5dsearch_parents_"+str(version)+".file", "wb") as f:
    pickle.dump(parents, f, pickle.HIGHEST_PROTOCOL)