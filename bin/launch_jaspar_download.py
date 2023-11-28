Last login: Tue Nov 28 11:13:53 on ttys002

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
avignoli@crgcomus-MacBook-Air:~$ cd Desktop/phd/test/
avignoli@crgcomus-MacBook-Air:~/Desktop/phd/test$ vim 
.DS_Store                        .nextflow.log.5                  exonerate/                       wise2/
.nextflow/                       .nextflow.log.6                  libapt-pkg-dev_1.6.17_amd64.deb  wise2.4.1/
.nextflow.log                    .nextflow.log.7                  mafft_7.511-1_amd64.deb          wise2.4.1.tar.gz
.nextflow.log.1                  .nextflow.log.8                  nextflow.config                  work/
.nextflow.log.2                  .nextflow.log.9                  requestJasparDatabase.py         
.nextflow.log.3                  apt_1.8.2.3_amd64.deb            test.nf                          
.nextflow.log.4                  download                         tets                             
avignoli@crgcomus-MacBook-Air:~/Desktop/phd/test$ vim requestJasparDatabase.py



























    parser.add_argument("-f", "--outputFormat", type=str, default="jaspar", help="Format of the output, by default \"jaspar\". Available formats are : \"json\", \"jsonp\", \"jaspar\", \"meme\", \"transfac\", \"pfm\" and \"yaml\" ") #bed not supported
    parser.add_argument("-a", "--cat", action="store_true", help="Use this option if you want to use the output to complete an existing file. It will remove the header of the first matrix")
    parser.add_argument("-u", "--apiUrl", type=str, default=API_URL, help="API URL. Use 'https://jaspar2020.genereg.net/api/v1/' if you want to get access to POLII collection.")
    return parser.parse_args()

def main():
    args = parseArgs()
    collection=args.collection
    name=args.name
    taxGroup=args.taxGroup
    taxId=args.taxId
    tfClass=args.tfClass
    tfFamily=args.tfFamily
    dataType=args.dataType
    version=args.version
    release=args.release
    outputFormat=args.outputFormat
    cat=args.cat
    apiUrl=args.apiUrl
    motifMatrixTxtGenerator=getMotifs(
        collection=collection,
        name=name,
        taxGroup=taxGroup,
        taxId=taxId,
        tfClass=tfClass,
        tfFamily=tfFamily,
        dataType=dataType,
        version=version,
        release=release,
        outputFormat=outputFormat,
        cat=cat,
        apiUrl=apiUrl
    )
    for matrixTxt in motifMatrixTxtGenerator :
        print(matrixTxt)

if __name__ == '__main__':
    main()
