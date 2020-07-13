CKPT_DIR="/home/fakanov/bert4rec/checkpoints"
data_dir="/home/fakanov/bert4rec/data/films/"
dataset_name="films"
max_seq_length=50
masked_lm_prob=0.2
max_predictions_per_seq=40

dim=64
batch_size=512
num_train_steps=100000

prop_sliding_window=0.5
mask_prob=1.0
dupe_factor=10
pool_size=10
use_bst=True
reg_coef=0

signature="-mp${mask_prob}-sw${prop_sliding_window}-mlp${masked_lm_prob}-df${dupe_factor}-mpps${max_predictions_per_seq}-msl${max_seq_length}"


#python -u ../gen_data_fin.py \
#    --data_dir=${data_dir} \
#    --dataset_name=${dataset_name} \
#    --max_seq_length=${max_seq_length} \
#    --max_predictions_per_seq=${max_predictions_per_seq} \
#    --mask_prob=${mask_prob} \
#    --dupe_factor=${dupe_factor} \
#    --masked_lm_prob=${masked_lm_prob} \
#    --prop_sliding_window=${prop_sliding_window} \
#    --signature=${signature} \
#    --pool_size=${pool_size} \
#    --use_bst=${use_bst} \

CUDA_VISIBLE_DEVICES=1 python -u ../run.py \
    --train_input_file=${data_dir}${dataset_name}${signature}.train.tfrecord \
    --test_input_file=${data_dir}${dataset_name}${signature}.test.tfrecord \
    --vocab_filename=${data_dir}${dataset_name}${signature}.vocab \
    --user_history_filename=${data_dir}${dataset_name}${signature}.his \
    --checkpointDir=${CKPT_DIR}/${dataset_name} \
    --signature=${signature}-${dim} \
    --do_train=False \
    --do_eval=True \
    --bert_config_file=../bert_configs/bert_config_${dataset_name}_${dim}.json \
    --batch_size=${batch_size} \
    --max_seq_length=${max_seq_length} \
    --max_predictions_per_seq=${max_predictions_per_seq} \
    --num_train_steps=${num_train_steps} \
    --num_warmup_steps=100 \
    --learning_rate=1e-4 \
    --use_bst=${use_bst} \
    --reg_coef=${reg_coef} \
