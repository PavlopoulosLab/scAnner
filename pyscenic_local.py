import sys,argparse,os,subprocess
from operator import itemgetter

def main(argv):
    parser = argparse.ArgumentParser(
                        description='Run the pyscenic GRN inference pipeline.',
                        epilog='')
    parser.add_argument('--loomFile', '-l', 
                        action='store',
                        type=str,
                        help='A valid loom file generated by SCopeLoomR R package.',
                        nargs='?', 
                        required=True)
    parser.add_argument('--outputFolder', '-o', 
                        action='store',
                        type=str,
                        const=os.getcwd(),
                        default=os.getcwd(),
                        help='The output folder path where the pyscenic results will be stored.',
                        nargs='?', 
                        required=False)
    parser.add_argument('--genomeBuild', '-g', 
                        action='store',
                        choices=['mm9', 'mm10', 'hg19', 'hg38'],
                        type=str,
                        nargs='?', 
                        help='The genome buid used during the alignment and counting step. Valid options are mm9, mm10, hg19, hg38', 
                        required=True)
    parser.add_argument('--annFolder', '-a', 
                        action='store',
                        type=str,
                        nargs='?', 
                        help='A folder containing all the mandatory annotation files, including ranking databases *.feather files, TF names file and motif annotation database *.tbl file.',
                        required=True)
    parser.add_argument('--threads', '-t', 
                        action='store',
                        type=int,
                        const=4,
                        default=4,
                        nargs='?', 
                        help='The number of threads to be used for each step of the analysis.',
                        required=False)
    parser.add_argument('--version', '-v', 
                        action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()
    try:
      args.loomFile
    except NameError:
      print ("Please provide a loom file of analyzed scRNA-seq dataset!")
      parser.print_help()
      sys.exit(1)
    try:
      args.annFolder
    except NameError:
      print ("Please provide a folder containing all the mandatory annotation files, including ranking databases *.feather files, TF names file and motif annotation database *.tbl file!")
      parser.print_help()
      sys.exit(1)
    if args.threads < 0:
        args.threads = 1
    if len(args.outputFolder) == 0:
        args.outputFolder = os.getcwd()
        print("Saving results to %s" % os.getcwd())
    feather1 = ""
    feather2 = ""
    tbl = ""
    TFs = ""
    adjacencies = ""
    nes = ""
    auc = ""
    if args.genomeBuild == "mm9":
        feather1 = args.annFolder+"/mm9-500bp-upstream-10species.mc9nr.feather"
        feather2 = args.annFolder+"/mm9-tss-centered-10kb-10species.mc9nr.feather"
        tbl = args.annFolder+"/motifs-v9-nr.mgi-m0.001-o0.0.tbl"
        TFs = args.annFolder+"/mm_mgi_tfs.txt"
        adjacencies = args.outputFolder+"/adjacencies.mm9.tsv"
        nes = args.outputFolder+"/nes.score.mm9.csv"
        auc = args.outputFolder+"/auc.mm9.loom"
        if not os.path.exists(feather1):
            print ("mm9-500bp-upstream-10species.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(feather2):
            print ("mm9-tss-centered-10kb-10species.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(tbl):
            print ("motifs-v9-nr.mgi-m0.001-o0.0.tbl is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(TFs):
            print ("mm_mgi_tfs.txt is not in %s!" % args.annFolder)
            sys.exit(1)
    if args.genomeBuild == "mm10":
        feather1 = args.annFolder+"/mm10__refseq-r80__500bp_up_and_100bp_down_tss.mc9nr.feather"
        feather2 = args.annFolder+"/mm10__refseq-r80__10kb_up_and_down_tss.mc9nr.feather"
        tbl = args.annFolder+"/motifs-v9-nr.mgi-m0.001-o0.0.tbl"
        TFs = args.annFolder+"/mm_mgi_tfs.txt"
        adjacencies = args.outputFolder+"/adjacencies.mm10.tsv"
        nes = args.outputFolder+"/nes.score.mm10.csv"
        auc = args.outputFolder+"/auc.mm10.loom"
        if not os.path.exists(feather1):
            print ("mm10__refseq-r80__500bp_up_and_100bp_down_tss.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(feather2):
            print ("mm10__refseq-r80__10kb_up_and_down_tss.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(tbl):
            print ("motifs-v9-nr.mgi-m0.001-o0.0.tbl is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(TFs):
            print ("mm_mgi_tfs.txt is not in %s!" % args.annFolder)
            sys.exit(1)
    if args.genomeBuild == "hg19":
        feather1 = args.annFolder+"/hg19-500bp-upstream-10species.mc9nr.feather"
        feather2 = args.annFolder+"/hg19-tss-centered-10kb-10species.mc9nr.feather"
        tbl = args.annFolder+"/motifs-v9-nr.hgnc-m0.001-o0.0.tbl"
        TFs = args.annFolder+"/hs_hgnc_curated_tfs.txt"
        adjacencies = args.outputFolder+"/adjacencies.hg19.tsv"
        nes = args.outputFolder+"/nes.score.hg19.csv"
        auc = args.outputFolder+"/auc.hg19.loom"
        if not os.path.exists(feather1):
            print ("mm10__refseq-r80__500bp_up_and_100bp_down_tss.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(feather2):
            print ("mm10__refseq-r80__10kb_up_and_down_tss.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(tbl):
            print ("motifs-v9-nr.hgnc-m0.001-o0.0.tbl is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(TFs):
            print ("hs_hgnc_curated_tfs.txt is not in %s!" % args.annFolder)
            sys.exit(1)
    if args.genomeBuild == "hg38":
        feather1 = args.annFolder+"/hg19-500bp-upstream-10species.mc9nr.feather"
        feather2 = args.annFolder+"/hg19-tss-centered-10kb-10species.mc9nr.feather"
        tbl = args.annFolder+"/motifs-v9-nr.hgnc-m0.001-o0.0.tbl"
        TFs = args.annFolder+"/hs_hgnc_curated_tfs.txt"
        adjacencies = args.outputFolder+"/adjacencies.hg38.tsv"
        nes = args.outputFolder+"/nes.score.hg38.csv"
        auc = args.outputFolder+"/auc.hg38.loom"
        if not os.path.exists(feather1):
            print ("hg38__refseq-r80__500bp_up_and_100bp_down_tss.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(feather2):
            print ("hg38__refseq-r80__10kb_up_and_down_tss.mc9nr.feather is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(tbl):
            print ("motifs-v9-nr.hgnc-m0.001-o0.0.tbl is not in %s!" % args.annFolder)
            sys.exit(1)
        if not os.path.exists(TFs):
            print ("hs_hgnc_curated_tfs.txt is not in %s!" % args.annFolder)
            sys.exit(1)
    try:
        #subprocess.run(['pyscenic', 'grn', args.loomFile, TFs,'--num_workers',args.threads,'--output',adjacencies])
        subprocess.check_call(['pyscenic', 'grn', args.loomFile, TFs,'--num_workers',str(args.threads),'--output',adjacencies])
    except subprocess.CalledProcessError:
        print("Error while running pyscenic grn!")
        sys.exit(1)
    try:
        #subprocess.run(['pyscenic', 'ctx','--annotations_fname', tbl, '--expression_mtx_fname',args.loomFile,'--output',nes,'--num_workers',args.threads,adjacencies,feather1,feather2])
        subprocess.check_call(['pyscenic', 'ctx','--annotations_fname', tbl, '--expression_mtx_fname',args.loomFile,'--output',nes,'--num_workers',str(args.threads),adjacencies,feather1,feather2])
    except subprocess.CalledProcessError:
        print("Error while running pyscenic ctx!")
        sys.exit(1)
    try:
        #subprocess.run(['pyscenic', 'aucell','-o', auc,'--num_workers',args.loomFile,nes])
        subprocess.check_call(['pyscenic', 'aucell','-o', auc,'--num_workers',str(args.threads),args.loomFile,nes])
    except subprocess.CalledProcessError:
        print("Error while running pyscenic aucell!")
        sys.exit(1)
    print("Pyscenic run was completed succesfully!")
if __name__ == "__main__":
   main(sys.argv[1:])
   

