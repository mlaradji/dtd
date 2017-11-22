with open("K5dsearch_version.file", "rb") as f:
    version = pickle.load(f)
    
with open("K5dsearch_Gseq_"+str(version)+".file", "rb") as f:
    Gseq = pickle.load(f)
    
with open("K5dsearch_SVseq_"+str(version)+".file", "rb") as f:
    SVseq = pickle.load(f) 
    
with open("K5dsearch_expanded_"+str(version)+".file", "rb") as f:
    expanded = pickle.load(f)
    
with open("K5dsearch_parents_"+str(version)+".file", "rb") as f:
    parents = pickle.load(f)