# CondReg: R package for condition number regularized covariance estimator

This repository hosts the R code implementation of the condition number regularized covariance estimator as an [R package](https://cran.r-project.org/package=CondReg): 

> Won, J.-H., Lim, J., Kim, S.-J. and Rajaratnam, B. (2013), Condition-number-regularized covariance estimation. Journal of the Royal Statistical Society: Series B (Statistical Methodology), 75: 427-450. [doi:10.1111/j.1467-9868.2012.01049.x](https://doi.org/10.1111/j.1467-9868.2012.01049.x)

## Installation

### CRAN published version

```R
install.packages("CondReg")
```

### Latest GitHub version

```R
devtools::install_github("dddlab/CondReg")
```

## Development

Container-based development environments are also specified in this repository. The relevant files are:
* Files in [`.devcontainer`](.devcontainer) directory
* [`docker-compose.yml`](docker-compose.yml) file

Above files allow deploying the development environments using GitHub Codespaces, Visual Studio Code, or Docker compose.

### Visual Studio Code

Development environment can be deployed on your local machine (Dev Containers) or remotely on GitHub Codespaces. GitHub Codespaces can be accessed through a web-based Visual Studio Code interface. If you have a local installation of Visual Studio Code, it can connect to both Dev Containers and GitHub Codespaces. 

#### GitHub Codespaces (Remote)

You will need [access to Codespaces](https://docs.github.com/en/codespaces/developing-in-codespaces/creating-a-codespace#access-to-codespaces) and enabled. Then, the files in [`.devcontainer`](.devcontainer) directory will do all the work!

#### Dev Container (Local)

Follow the [Remote Development in Containers tutorial](https://code.visualstudio.com/docs/remote/containers-tutorial)

### Docker Compose

Here are the steps:

```bash
# Clone this repository
git clone https://github.com/dddlab/CondReg
cd CondReg

# Build image and start container
docker-compose build CondReg
docker-compose up
```
Find and click on a link similar to 
```
http://127.0.0.1:8888/lab?token=[generated token string]
```
and start your RStudio.

### Repository File Location
Due to the differences in working directory settings ([`workspaceFolder`](https://code.visualstudio.com/docs/remote/devcontainerjson-reference#_image-or-dockerfile-specific-properties) is not implemented in GitHub Codespaces), the path to the workspace folder is `/workspaces/CondReg`. 

Since `/workspaces` directory is not writable by `jovyan` user, building and checking the R package would not work from `/workspaces` directory. Instead, there is a symbolic link directory `/home/jovyan/work` is also created. You would need to switch to `/home/jovyan` in order to build and check the R package:
```bash
cd /home/jovyan
R CMD build work
R CMD check CondReg_[version-number].tar.gz
```