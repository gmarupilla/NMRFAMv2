STAN_MODEL_ADJUSTING = """
data
{
int is_it_final;
int LENGTH;
int final_size;
vector [final_size] scales_mat_est;


matrix [final_size , final_size] temps_square_dots;

vector [final_size] temps_mixture_dots ;
vector [final_size] zeros ; 

vector [final_size] sigma ;

vector [final_size] scales_mean ;
vector [final_size] scales_sigma ;
}
parameters
{
vector <lower = 0.001 , upper = 1000000000 > [final_size] scales;
}
model
{
scales ~ normal(scales_mean , scales_sigma);
zeros ~ normal( (temps_mixture_dots - (temps_square_dots * scales)), sigma);
}
"""

# INITIALESTIMATE
STAN_MODEL_BASIC = """
data
{
int is_it_final;
int LENGTH;    //2048
int final_size; //5
vector  [final_size] scales_mat_est ;    // Grant's estimations for the scale values


matrix [final_size , final_size] temps_square_dots;  // dot product of each template with itself

//row_vector [final_size] temps_mixture_dots ;  // dot product of each template with the mixture
vector [final_size] temps_mixture_dots ;  // dot product of each template with the mixture
//row_vector [final_size] zeros;   // a list of zeros with the same size as the number of the matabolites and scales
vector [final_size] zeros;   // a list of zeros with the same size as the number of the matabolites and scales


vector [final_size] sigma ;     //list of small numbers

//matrix [final_size,final_size] scales_mean ;   // diagonal scales_mat_est rest of it zero
//matrix [final_size,final_size] scales_sigma;    // diagonal scales_mat_est * 2 rest of it zero

//row_vector  [final_size] scales_mean ;
vector  [final_size] scales_mean ;
//row_vector  [final_size] scales_sigma ;
vector  [final_size] scales_sigma ;

}

parameters
{
//row_vector  <lower = 0.001 , upper = 100000 > [final_size] scales;   // scale values
vector  <lower = 0.001 , upper = 1000000 > [final_size] scales;   // scale values


}


model
{

    scales  ~ normal(scales_mean ,2 * scales_sigma);
        
    
    //correct one
    zeros ~ normal (  (temps_mixture_dots - (temps_square_dots * scales)) , sigma );
}

"""

# REESTIMATE
STAN_MODEL_BAD_ESTIMATES = """
data
{
int is_it_final;
int LENGTH;    //2048
int final_size; //5
vector  [final_size] scales_mat_est ;    // Grant's estimations for the scale values


matrix [final_size , final_size] temps_square_dots;  // dot product of each template with itself

//row_vector [final_size] temps_mixture_dots ;  // dot product of each template with the mixture
vector [final_size] temps_mixture_dots ;  // dot product of each template with the mixture
//row_vector [final_size] zeros;   // a list of zeros with the same size as the number of the matabolites and scales
vector [final_size] zeros;   // a list of zeros with the same size as the number of the matabolites and scales


vector [final_size] sigma ;     //list of small numbers

//matrix [final_size,final_size] scales_mean ;   // diagonal scales_mat_est rest of it zero
//matrix [final_size,final_size] scales_sigma;    // diagonal scales_mat_est * 2 rest of it zero

//row_vector  [final_size] scales_mean ;
vector  [final_size] scales_mean ;
//row_vector  [final_size] scales_sigma ;
vector  [final_size] scales_sigma ;

}

parameters
{
//row_vector  <lower = 0.001 , upper = 100000 > [final_size] scales;   // scale values
vector  <lower = 0.001 , upper = 1000000 > [final_size] scales;   // scale values


}


model
{

    scales  ~ normal(10 * scales_mean ,4 * scales_sigma);
        
    
    //correct one
    zeros ~ normal (  (temps_mixture_dots - (temps_square_dots * scales)) , sigma );
}

"""
# ALTERNATIVEESTIMATES
STAN_MODEL_OK_ESTIMATES = """
data
{
int is_it_final;
int LENGTH;    //2048
int final_size; //5
vector  [final_size] scales_mat_est ;    // Grant's estimations for the scale values


matrix [final_size , final_size] temps_square_dots;  // dot product of each template with itself

//row_vector [final_size] temps_mixture_dots ;  // dot product of each template with the mixture
vector [final_size] temps_mixture_dots ;  // dot product of each template with the mixture
//row_vector [final_size] zeros;   // a list of zeros with the same size as the number of the matabolites and scales
vector [final_size] zeros;   // a list of zeros with the same size as the number of the matabolites and scales


vector [final_size] sigma ;     //list of small numbers

//matrix [final_size,final_size] scales_mean ;   // diagonal scales_mat_est rest of it zero
//matrix [final_size,final_size] scales_sigma;    // diagonal scales_mat_est * 2 rest of it zero

//row_vector  [final_size] scales_mean ;
vector  [final_size] scales_mean ;
//row_vector  [final_size] scales_sigma ;
vector  [final_size] scales_sigma ;

}

parameters
{
//row_vector  <lower = 0.001 , upper = 100000 > [final_size] scales;   // scale values
vector  <lower = 0.001 , upper = 1000000 > [final_size] scales;   // scale values


}


model
{

    scales  ~ normal(4 * scales_mean ,2 * scales_sigma);
        
    
    //correct one
    zeros ~ normal (  (temps_mixture_dots - (temps_square_dots * scales)) , sigma );
}

"""
