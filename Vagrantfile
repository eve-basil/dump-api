# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "dumpapi.basil.devbox"
  #config.vm.network "private_network", ip: "192.168.77.11"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "dump-api.basil.devbox"
  end

  config.vm.provision "file", source: "../openrc", destination: ".openrc"
  config.vm.provision "file", source: "~/.gitconfig", destination: ".gitconfig"
  config.vm.provision "file", source: "~/.ssh/id_rsa", destination: ".ssh/id_rsa"
#  config.vm.provision "file", source: "provisioning/ssh_config", destination: ".ssh/config"
#  config.vm.provision "file", source: "provisioning/ansible.cfg", destination: ".ansible.cfg"
#  config.vm.provision "file", source: "provisioning/inventory", destination: ".ansible_inventory"

#  config.vm.provision "shell", path: "provisioning/provision.sh", name: "Finishing provision work."

# wrapt

end
