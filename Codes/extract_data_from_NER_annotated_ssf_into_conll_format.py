# how to run the code
# python3 extract_raw_sentences_from_SSF.py --input InputFolderPath --output OutputFolderPath
# no need to create a output folder, only give a name
# author : Pruthwik Mishra, LTRC, IIIT-H
import ssfAPI_ner as ssf
import argparse
# from random import shuffle


def readFilesAndExtractNERInConLL(inputFolderPath, outputPath):
    fileList = ssf.folderWalk(inputFolderPath)
    newFileList = []
    for fileName in fileList:
        xFileName = fileName.split('/')[-1]
        if xFileName == 'err.txt' or xFileName.split('.')[-1] in ['comments', 'bak'] or xFileName[:4] == 'task':
            continue
        else:
            newFileList.append(fileName)
    newFileList = sorted(newFileList)
    sentencesList = list()
    for fileName in newFileList:
        print(fileName)
        d = ssf.Document(fileName)
        for tree in d.nodeList:
            tokensWithNER = list()
            rootNode = tree.nodeList[0]
            for node in rootNode.nodeList:
                if node.type:
                    nerType = node.getAttribute('ne')
                    for index, tok in enumerate(node.nodeList):
                        if not nerType:
                            tokensWithNER.append(tok.lex + '\tO')
                        else:
                            if index == 0:
                                tokensWithNER.append(tok.lex + '\tB-' + nerType)
                            else:
                                tokensWithNER.append(tok.lex + '\tI-' + nerType)
                else:
                    tokensWithNER.append(node.lex + '\tO')
            sentencesList.append('\n'.join(tokensWithNER) + '\n')
    writeListToFile(sentencesList, outputPath)


def writeListToFile(dataList, outFilePath):
    with open(outFilePath, 'w', encoding='utf-8') as fileWrite:
        fileWrite.write('\n'.join(dataList) + '\n')
        fileWrite.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp',
                        help="Add the input folder path")
    parser.add_argument('--output', dest='out',
                        help="Add the output file path where NER data in conll format will be written")
    args = parser.parse_args()
    readFilesAndExtractNERInConLL(args.inp, args.out)
