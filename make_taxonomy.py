import pandas as pd


LEVEL = 100

taxonomy_file_data = []

main_dict = dict()

def get_all(D, i):
  if not D:
    return
  main_dict[i] = list(D.keys())
  for i,j in D.items():
    main_dict[i] = list(j.keys())
    get_all(j, i)
  return

def create(taxonomy):
    traversals = taxonomy['sector_id'].tolist()
    rev_traversals = []
    for i in traversals:
        s = i.split(">>")
        revs = s[:LEVEL][::-1]
        rev_traversals.append(revs)
    return rev_traversals


def formTree(list): 
    tree = {} 
    for item in list: 
        currTree = tree
        for key in item[::-1]: 
            if key not in currTree: 
                currTree[key] = {} 
            currTree = currTree[key] 
              
    return tree

def make_taxonomy_file(t,k):
  if not t.keys():
    return
  if k == 'Root':
    l = ['Root'] + list(t.keys())
    taxonomy_file_data.append(l)
    for i in t.keys():
      if type(t[i]) == dict:
        make_taxonomy_file(t[i], i)
  else:
    l = [k] + list(t.keys())
    taxonomy_file_data.append(l)
    for i in t.keys():
        make_taxonomy_file(t[i], i)
  return

def create_id2tag(taxonomy):
    id_2_Tag = dict()
    count = 0
    for i, val in taxonomy.iterrows():
    ids = val['sector_id'].split(">>")
    sector = val['sector'].split(">>")
    for idx in range(0,len(ids)):
        try:
            id_2_Tag[ids[idx]] = sector[idx]
            count += 1
        except:
            print("Skipped a data record because disbalanced columns")
    print(f"{count} number of datapoints recieved")
    return id_2_Tag


if __name__ == "__main__":
    taxonomy = pd.read_csv("data/taxonomy.csv")
    taxonomy = taxonomy[~taxonomy.sector.str.contains("Orphan")]
    rev_traversals = create(taxonomy)
    id2tag = create_id2tag(taxonomy)
    tree = formTree(rev_traversals)
    make_taxonomy_file(tree, 'Root')
    with open('data/rcv1.taxonomy', 'w') as f:
        for item in taxonomy_file_data:
            f.write("%s\n" % '\t'.join(item))
    get_all(tree, 'Root')
    with open(f"data/parent_child.json", "w") as outfile: 
      json_obj = json.dumps(main_dict)
      outfile.write(json_obj)