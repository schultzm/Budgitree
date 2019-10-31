Vagrant.configure("2") do |config|
  config.vm.box = "sylabs/singularity-3.2-ubuntu-bionic64"
  config.vm.box_version = "20190529.0.0"
  config.vm.provision :shell, path: "vagrant_scripts/bootstrap.sh"
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end
end
