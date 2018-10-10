import sys
import numpy as np
class Node():
  """A node in the suffix tree.

  value
      As a identifier, custom for each node except leav nodes
  """
  def __init__(self,value = "$"):
      self.part_of_string = []
      self.edges = []
      self.identifier = value

  def set_part_of_string(self,num):
      """
      Defines which substring is "part" of the node
      """
      self.part_of_string.append(num)

  def set_edges(self,edge):
      """
      the edge set of the node
      """
      self.edges.append(edge)

  def __repr__(self):
      return "Node : {}\n  Part of string: {} \n  Children: {}".format(self.identifier,self.part_of_string,self.edges)


class Edge():
    """
    An Edge in the suffix tree

    value
        The value/label of the edge

    parrent_node
        The node at which the edge starts

    child_node
        The Node where the edge is heading to /ending
    """

    def __init__(self, value,parrent_node, child_node=Node(), end_edge=False):
        self.value= value
        self.from_node = parrent_node
        self.to_node = child_node
        self.end_edge = end_edge

    def set_to_node(self,node):
        """
        Sets the Node to which the edge is heading
        """
        self.to_node = node

    def __repr__(self):
        return "Value: {}, From Node: {}, To Node: {}\n".format(self.value,self.from_node.identifier,self.to_node.identifier)
class GenralizedSuffixTree():
  """
  A naiv implementation of the generalized suffix tree
  """
  def __init__(self,sequences):
      """
      sequences
          A list of strings which should be added to the GST

      identifier
          Starting identifier to label the nodes

      root
          root node of the GST
      """
      self.sequences = sequences
      self.node_identifier = 0
      self.root = Node(0)


  def add_suffix(self,suffix,part_of_string):
      """
          Adds Suffix to the existing SuffixTree

          suffix:
              a suffix of a sequence

          part_of_string:
              number indicating to which sequence the current suffix belongs
      """
      suffix = suffix
      suffix_length=len(suffix)

      current_node = self.root

      for number, char in enumerate(suffix):

          edges = [edge.value for edge in current_node.edges]


          if char not in edges:

              self.node_identifier += 1

              child_node = Node(self.node_identifier)

              if suffix_length == number+1:
                  child_node.set_part_of_string(part_of_string)
                  new_edge = Edge(char,current_node,child_node,True)
              else:
                  new_edge = Edge(char,current_node,child_node)
              current_node.set_edges(new_edge)
              current_node= child_node

          else:
              for edge in current_node.edges:
                  if char == edge.value:
                      if suffix_length == number+1:
                          edge.end_edge = True
                          current_node = edge.to_node
                          current_node.set_part_of_string(part_of_string)
                      else:
                          current_node = edge.to_node

                      break


  def add_suffix_with_text(self,suffix,part_of_string):
          """
              Adds Suffix to the existing SuffixTree

              suffix:
                  a suffix of a sequence

              part_of_string:
                  number indicating to which sequence the current suffix belongs
          """
          suffix = suffix
          suffix_length=len(suffix)
          print("\n o '{}' with length {}".format(suffix, suffix_length))

          current_node = self.root

          for number, char in enumerate(suffix):
              print(" Current Char : ",char, "' (with pos",number+1,"in suffix)")

              edges = [edge.value for edge in current_node.edges]


              if char not in edges:
                  print("  ",char," not in Edge set: ",edges)

                  self.node_identifier += 1

                  child_node = Node(self.node_identifier)

                  if suffix_length == number+1:
                      child_node.set_part_of_string(part_of_string)
                      new_edge = Edge(char,current_node,child_node,True)
                      print("    (Char is end node)")
                  else:
                      new_edge = Edge(char,current_node,child_node)
                      print("    (Char is no end node)")

                  visual = "    {} {}\n    |{}\n    {} {}".format(current_node.identifier,current_node.part_of_string,char,child_node.identifier,child_node.part_of_string)
                  if suffix_length == number+1:
                      visual = visual+" $"
                  print(visual)
                  current_node.set_edges(new_edge)
                  current_node= child_node

              else:
                  print("  ",char," is  in Edge set: ",edges)
                  if suffix_length == number+1:
                      print("    (Char is end node)")
                  else:
                      print("    (Char is no end node)")

                  for edge in current_node.edges:
                      if char == edge.value:

                          puffer = current_node
                          if suffix_length == number+1:
                              edge.end_edge = True
                              current_node = edge.to_node
                              current_node.set_part_of_string(part_of_string)
                          else:
                              current_node = edge.to_node

                          visual = "    {} {}\n    |{}\n    {} {}".format(puffer.identifier,puffer.part_of_string,char,current_node.identifier,current_node.part_of_string)
                          if suffix_length == number+1:
                              visual = visual+" $"
                          print(visual)

                          break





  def construct_tree(self,with_text=False):
      """
      Constructs the tree given the input Sequences using the add function

      with_text
          If true, Text displays what is done in each step, where $ displays that node is a end node
      """
      for part_of_string, seq in enumerate(self.sequences):
          if part_of_string%10000==0:
              print(part_of_string,"/",len(self.sequences))
          for suffix in self.suffix(seq):
              if with_text:
                  self.add_suffix_with_text(suffix,part_of_string)
              else:
                  self.add_suffix(suffix,part_of_string)

      return self


  def prefix(self,string):
      """
      Given a string, yield all the prefixes of the string starting by the whole string
      """
      for i in range(len(string)):
          string_to_yield = string
          string = string[:-1]
          yield string_to_yield

  def suffix(self,string):
      """
      Given a string, yield all the suffixes of the string starting with the whole string
      """
      end = len(string)
      for i in range(end):
          yield string[i:end]

  def search_all_prefixes(self, pattern):
      for prefix in self.prefix(pattern):
          hit , in_seq = self.search(prefix)
          if hit:
              print(prefix," found in",len(np.unique(in_seq))," Sequences. Seq: ",np.unique(in_seq))

  def search(self, pattern):
      """
      Given a pattern, look if any prefix of the pattern is in the GST

      pattern
          the pattern we want to search for
      """
      for prefix in self.prefix(pattern):
          current_node = self.root
          current_edge = None

          if not current_node.edges:
              return False , []

          for char in prefix:
              char_not_found = True
              for edge in current_node.edges:
                  if char == edge.value:
                      char_not_found = False
                      current_edge = edge
                      current_node = edge.to_node
                      break
              if char_not_found:
                  return False , []

          if current_edge.end_edge:
               return True, [num +1 for num in current_node.part_of_string]
          else:
              return False, []

def main():
    with open(str(sys.argv[1]),"r") as seq:
        Sequences = seq.readlines()
    Sequences = [seq[:-1] for seq in Sequences]

    tree = GenralizedSuffixTree(Sequences).construct_tree()

    tree.search_all_prefixes(str(sys.argv[2]))



if __name__ == "__main__":
    main()
