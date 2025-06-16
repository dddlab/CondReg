pkgname <- "condregR"
source(file.path(R.home("share"), "R", "examples-header.R"))
options(warn = 1)
base::assign(".ExTimings", "condregR-Ex.timings", pos = 'CheckExEnv')
base::cat("name\tuser\tsystem\telapsed\n", file=base::get(".ExTimings", pos = 'CheckExEnv'))
base::assign(".format_ptime",
function(x) {
  if(!is.na(x[4L])) x[1L] <- x[1L] + x[4L]
  if(!is.na(x[5L])) x[2L] <- x[2L] + x[5L]
  options(OutDec = '.')
  format(x[1L:3L], digits = 7L)
},
pos = 'CheckExEnv')

### * </HEADER>
library('condregR')

base::assign(".oldSearch", base::search(), pos = 'CheckExEnv')
base::assign(".old_wd", base::getwd(), pos = 'CheckExEnv')
cleanEx()
nameEx("condreg")
### * condreg

flush(stderr()); flush(stdout())

base::assign(".ptime", proc.time(), pos = "CheckExEnv")
### Name: condreg
### Title: Condition Number Regularized Covariance Estimation
### Aliases: condreg

### ** Examples

## Generate example data
set.seed(123)
X <- matrix(rnorm(100*5), 100, 5)

## Regularize with condition number bound of 10
result <- condreg(X, 10)

## Examine resulting matrices
cov_matrix <- result$S
precision_matrix <- result$invS

## Check condition number
eigenvals <- eigen(cov_matrix, only.values=TRUE)$values
condition_number <- max(eigenvals)/min(eigenvals)
print(condition_number)  # Should be <= 10

## Example with true covariance matrix
sigma <- diag(5)
sigma[3,2] <- sigma[2,3] <- 0.8

## Not run: 
##D library(MASS)
##D X <- mvrnorm(200, rep(0,5), sigma)
##D 
##D ## Covariance estimation
##D crcov <- condreg(X, 3)
##D 
##D ## Inspect output
##D str(crcov)              ## returned object
##D sigma.hat <- crcov$S    ## estimate of sigma matrix
##D omega.hat <- crcov$invS ## estimate of inverse of sigma matrix
## End(Not run)



base::assign(".dptime", (proc.time() - get(".ptime", pos = "CheckExEnv")), pos = "CheckExEnv")
base::cat("condreg", base::get(".format_ptime", pos = 'CheckExEnv')(get(".dptime", pos = "CheckExEnv")), "\n", file=base::get(".ExTimings", pos = 'CheckExEnv'), append=TRUE, sep="\t")
cleanEx()
nameEx("kgrid")
### * kgrid

flush(stderr()); flush(stdout())

base::assign(".ptime", proc.time(), pos = "CheckExEnv")
### Name: kgrid
### Title: Return a vector of grid of penalties for cross-validation
### Aliases: kgrid

### ** Examples

gmax <- 20 ## maximum value for the grid of points
npts <- 10 ## number of grid points returned
gridpts <- kgrid(gmax,npts)



base::assign(".dptime", (proc.time() - get(".ptime", pos = "CheckExEnv")), pos = "CheckExEnv")
base::cat("kgrid", base::get(".format_ptime", pos = 'CheckExEnv')(get(".dptime", pos = "CheckExEnv")), "\n", file=base::get(".ExTimings", pos = 'CheckExEnv'), append=TRUE, sep="\t")
cleanEx()
nameEx("select_condreg")
### * select_condreg

flush(stderr()); flush(stdout())

base::assign(".ptime", proc.time(), pos = "CheckExEnv")
### Name: select_condreg
### Title: Compute the best condition number regularized based based on
###   cross-validation selected penalty parameter
### Aliases: select_condreg

### ** Examples

## True covariance matrix
sigma <- diag(5)
sigma[3,2] <- sigma[2,3] <- 0.8

## Generate normal random samples
## Not run: 
##D library(MASS)
##D X <- mvrnorm(200,rep(0,5),sigma)
##D 
##D ## Covariance estimation
##D gridpts <- kgrid(50,100)           ## generate grid of penalties to search over
##D crcov <- select_condreg(X,gridpts) ## automatically selects penalty parameter
##D 
##D ## Inspect output
##D str(crcov)              ## returned object
##D sigma.hat <- crcov$S    ## estimate of sigma matrix
##D omega.hat <- crcov$invS ## estimate of inverse of sigma matrix
## End(Not run)



base::assign(".dptime", (proc.time() - get(".ptime", pos = "CheckExEnv")), pos = "CheckExEnv")
base::cat("select_condreg", base::get(".format_ptime", pos = 'CheckExEnv')(get(".dptime", pos = "CheckExEnv")), "\n", file=base::get(".ExTimings", pos = 'CheckExEnv'), append=TRUE, sep="\t")
cleanEx()
nameEx("select_kmax")
### * select_kmax

flush(stderr()); flush(stdout())

base::assign(".ptime", proc.time(), pos = "CheckExEnv")
### Name: select_kmax
### Title: Selection of penalty parameter based on cross-validation
### Aliases: select_kmax

### ** Examples

## Not run: 
##D # Generate random data
##D X <- matrix(rnorm(500), 100, 5)
##D 
##D # Create penalty grid
##D k_grid <- kgrid(50, 20)
##D 
##D # Find optimal penalty
##D result <- select_kmax(X, k_grid)
##D optimal_k <- result$kmax
## End(Not run)



base::assign(".dptime", (proc.time() - get(".ptime", pos = "CheckExEnv")), pos = "CheckExEnv")
base::cat("select_kmax", base::get(".format_ptime", pos = 'CheckExEnv')(get(".dptime", pos = "CheckExEnv")), "\n", file=base::get(".ExTimings", pos = 'CheckExEnv'), append=TRUE, sep="\t")
### * <FOOTER>
###
cleanEx()
options(digits = 7L)
base::cat("Time elapsed: ", proc.time() - base::get("ptime", pos = 'CheckExEnv'),"\n")
grDevices::dev.off()
###
### Local variables: ***
### mode: outline-minor ***
### outline-regexp: "\\(> \\)?### [*]+" ***
### End: ***
quit('no')
