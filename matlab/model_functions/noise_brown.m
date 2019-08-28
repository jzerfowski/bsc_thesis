function [Ie_noise, Ii_noise] = noise_brown(dt, reg, tnumb, noiseseed, noiseamp, noisecor, tau, Ienoise, Iinoise)
%BROWNIAN_NOISE Summary of this function goes here
%   Detailed explanation goes here

s = RandStream('mcg16807','Seed', noiseseed);
RandStream.setGlobalStream(s);

alpha = 1-dt/tau;
afil = [1 -alpha];
bfil = 1;
nsigb = zeros(reg, tnumb);
for r = 1:reg % because of 1D filter function
    randsig = noiseamp * 0.5*randn(1,tnumb);
    nsigb(r,:) = filter(bfil,afil,randsig)*sqrt(1-alpha);
    nsigb(r,:) = noiseamp*0.1 - mean(nsigb(r,:)) + nsigb(r,:);
end
nsigb(reg,:) = noisecor*nsigb(1,:) + (1-noisecor)*nsigb(reg,:);
Ii_noise = single(bsxfun(@times,Iinoise(1:reg)',nsigb));
Ie_noise = single(bsxfun(@times,Ienoise(1:reg)',nsigb));
clear nsigb

end

