#!/bin/bash

# some options to
WGET_OPTS="-nv --show-progress --progress=dot:giga"

echo "###"
echo " "
echo "Welcome to a microbial genomics QC pipeline using Snakemake and Singularity..."
echo " "

echo "For any issues, please post them to https://github.com/andersgs/rcpa_wgs_ptp"

echo " "

echo "Checking for snakemake..."

conda="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"

[ -n "$(which snakemake)" ] && echo "** Found Snakemake" ||
    echo "Could not find Snakemake. You can run the following to install it:
    wget -O conda.sh $conda && bash conda.sh -b -p $HOME/miniconda3 && export PATH=$HOME/miniconda3/bin:$PATH && rm conda.sh && conda -c bioconda install snakemake psutil"

echo " "
echo "Checking for Singularity..."

[ -n "$(which singularity)" ] && echo "** Found Singularity" ||
    echo "Could not find Singularity installed. Please follow instructions here: https://www.sylabs.io/guides/3.1/user-guide/installation.html#install-on-linux"

echo " "
echo "Downloading singularity images (~13.5 GB of data)..."
echo "This may take some time... Please be patient."

abricate="https://cloudstor.aarnet.edu.au/plus/s/mSFAIjqlMQPxzRu/download"
asm="https://cloudstor.aarnet.edu.au/plus/s/7ZhlUM1fZeqKaRR/download"
kmer_counter="https://cloudstor.aarnet.edu.au/plus/s/U30bRdQ9CQPw7FD/download"
kraken="https://cloudstor.aarnet.edu.au/plus/s/4e67yqkw8vMZEM7/download"
mlst="https://cloudstor.aarnet.edu.au/plus/s/27uRCqbco9ep8Mp/download"
read_assessment="https://cloudstor.aarnet.edu.au/plus/s/YoU7tmVBepPzW5F/download"
asm_assessment="https://cloudstor.aarnet.edu.au/plus/s/Rxza7lYHWGtzCp4/download"
serotyping="https://cloudstor.aarnet.edu.au/plus/s/JEg6CzEZaMAvCcy/download"

mkdir -p pipelines/singularity_images && cd pipelines/singularity_images
[ ! -f "abricate.simg" ] && echo "** Starting download of abricate..." && wget ${WGET_OPTS} -O "abricate.simg" $abricate || echo "** abricate.simg already downloaded."
[ ! -f "asm.simg" ] && echo "** Starting download of assembler..." && wget ${WGET_OPTS} -O "asm.simg" $asm || echo "** asm.simg already downloaded. skipping..."
[ ! -f "kmer_counters.simg" ] && echo "** Starting download of kmer counters..." && wget ${WGET_OPTS} -O "kmer_counters.simg" $kmer_counter || echo "** kmer_counters.simg already downloaded. skipping..."
[ ! -f "kraken2.simg" ] && echo "** Starting download of kraken..." && wget ${WGET_OPTS} -O "kraken2.simg" $kraken || echo "** kraken2.simg already downloaded. skipping..."
[ ! -f "mlst.simg" ] && echo "** Starting download of mlst..." && wget ${WGET_OPTS} -O "mlst.simg" $mlst || echo "** mlst.simg already downloaded. skipping..."
[ ! -f "read_assessment.simg" ] && echo "** Staring download of read assessment..." && wget ${WGET_OPTS} -O "read_assessment.simg" $read_assessment || echo "** read_assessment.simg already downloaded. skipping..."
[ ! -f "asm_assessment.simg" ] && echo "** Staring download of assembly assessement..." && wget ${WGET_OPTS} -O "asm_assessment.simg" $asm_assessment || echo "** asm_assessment.simg already downloaded. skipping..."
[ ! -f "serotyping.simg" ] && echo "** Starting download of serotyping..." && wget ${WGET_OPTS} -O "serotyping.simg" $serotyping || echo "** serotyping.simg already downloaded. skipping..."
cd ../..

echo " "
echo "Now downloading some test data (Salmonella Typhimurium and Salmonella Enteritidis)."

mkdir -p data && cd data

echo " "
echo "Downloading ERR1305793..."

r1="ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR130/ERR1305793/lib113-STM-LT2_S19_L001_R1_001.fastq.gz"
r2="ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR130/ERR1305793/lib113-STM-LT2_S19_L001_R2_001.fastq.gz"

mkdir -p ERR1305793 && cd ERR1305793
[ ! -f "R1.fq.gz" ] && wget ${WGET_OPTS} -O R1.fq.gz $r1 || echo "** ERR1305793 R1 already downloaded. skipping..."
[ ! -f "R2.fq.gz" ] && wget ${WGET_OPTS} -O R2.fq.gz $r2 || echo "** ERR1305793 R2 already downloaded. skipping..."

cd ..

echo " "
echo "Downloading SRR5381280..."

r1="ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR538/000/SRR5381280/SRR5381280_1.fastq.gz"
r2="ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR538/000/SRR5381280/SRR5381280_2.fastq.gz"

mkdir -p SRR5381280 && cd SRR5381280
[ ! -f "R1.fq.gz" ] && wget ${WGET_OPTS} -O R1.fq.gz $r1 || echo "** SRR5381280 R1 already downloaded. skipping..."
[ ! -f "R2.fq.gz" ] && wget ${WGET_OPTS} -O R2.fq.gz $r2 || echo "** SRR5381280 R2 already downloaded. skipping..."

cd ..

echo " "
echo "Making a negative control..."
echo "Making R1..."
mkdir -p ntc_reads && cd ntc_reads
zcat ../SRR5381280/R1.fq.gz | head -n 2000 | gzip > R1.fq.gz
zcat ../ERR1305793/R1.fq.gz | head -n 2000 | gzip >> R1.fq.gz

echo "Making R2..."
zcat ../SRR5381280/R2.fq.gz | head -n 2000 | gzip > R2.fq.gz
zcat ../ERR1305793/R2.fq.gz | head -n 2000 | gzip >> R2.fq.gz

echo "Negative control ready..."
echo " "

cd ..

echo "Preparing input table..."
echo -e "SAMPLE_ID\tR1\tR2\tSAMPLE_TYPE" > input.tab

for sample in ERR1305793 SRR5381280 ntc_reads; do
    [ "ntc_reads" == "${sample}" ] && sample_type="ntc" || sample_type="data"
    echo -e "lab99-${sample}\t$(realpath ${sample}/R1.fq.gz)\t$(realpath ${sample}/R2.fq.gz)\t${sample_type}" >> input.tab
done

mv input.tab ../pipelines

cd ..

echo " "
echo "Startup finished..."
echo "You can now run the pipeline with the following command: cd pipelines && snakemake --use-singularity."

echo " "
echo "###"
